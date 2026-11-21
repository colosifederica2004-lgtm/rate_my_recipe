"""Analyse recipe ratings and calculate recipe-level statistics."""

import numpy as np
import pandas as pd
from recipe_project.ranking import (
    bayesian_weighted_ranking,
    simple_average_ranking,
)

from recipe_project.cleaning import filter_valid_interactions
from recipe_project.data_loader import load_interactions, load_recipes


DEFAULT_SEED = 42


def _validate_interactions(interactions):
    """Validate the structure and contents of an interactions DataFrame."""

    if not isinstance(interactions, pd.DataFrame):
        raise TypeError("interactions must be a pandas DataFrame.")

    required_columns = {"recipe_id", "rating"}

    missing_columns = required_columns - set(interactions.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    if interactions.empty:
        raise ValueError("interactions DataFrame is empty.")

    if interactions[["recipe_id", "rating"]].isnull().any().any():
        raise ValueError(
            "recipe_id and rating cannot contain missing values."
        )

    if not pd.api.types.is_numeric_dtype(interactions["rating"]):
        raise TypeError("rating must be numeric.")

    if not interactions["rating"].between(1, 5).all():
        raise ValueError("Ratings must be between 1 and 5.")


def calculate_recipe_stats(valid_interactions):
    """
    Calculate the number of ratings and the average rating for each recipe.

    Parameters
    ----------
    valid_interactions : pandas.DataFrame
        Interactions containing only valid ratings (from 1 to 5).

    Returns
    -------
    pandas.DataFrame
        A DataFrame with one row per recipe and three columns:
        recipe_id, rating_count and average_rating.
    """
    _validate_interactions(valid_interactions)

    recipe_stats = (
        valid_interactions
        .groupby("recipe_id")
        .agg(
            rating_count=("rating", "count"),
            average_rating=("rating", "mean")
        )
        .reset_index()
    )

    return recipe_stats


# Fixed seed: the random split is the same every time the code is run
def split_train_test(interactions, train_fraction=0.5, seed=DEFAULT_SEED):
    """
    Randomly split the ratings into a train and a test set.

    Parameters
    ----------
    interactions : pandas.DataFrame
        Interactions containing valid ratings.
    train_fraction : float, optional
        Approximate share of ratings assigned to the train set.
    seed : int, optional
        Seed of the random number generator, to get a reproducible split.

    Returns
    -------
    tuple of pandas.DataFrame
        The train set and the test set.

    Raises
    ------
    ValueError
        If train_fraction is not strictly between 0 and 1.
    """
    _validate_interactions(interactions)

    if not 0 < train_fraction < 1:
        raise ValueError("train_fraction must be between 0 and 1")

    if not isinstance(seed, (int, np.integer)):
        raise TypeError("seed must be an integer.")

    n_rows = len(interactions)

    if n_rows < 2:
        raise ValueError(
            "At least two interactions are required for splitting."
        )

    rng = np.random.default_rng(seed)

    is_train = rng.random(n_rows) < train_fraction

    train = interactions.iloc[is_train].copy()
    test = interactions.iloc[~is_train].copy()

    return train, test


def build_evaluation_table(train, test):
    """Build a table with train statistics and test information per recipe.
    
    Every recipe of the train set is kept, together with the statistics computed on the train set and the information on its test ratings.

    Parameters
    ----------
    train : pandas.DataFrame
        Train set of valid ratings.
    test : pandas.DataFrame
        Test set of valid ratings.

    Returns
    -------
    pandas.DataFrame
        One row per recipe of the train set, with the columns recipe_id,
        rating_count and average_rating (computed on the train set) and
        test_sum and test_count (sum and number of the test ratings,
        0 if the recipe has no test ratings).
    """

    _validate_interactions(train)
    _validate_interactions(test)

    recipe_stats = calculate_recipe_stats(train)

    test_stats = (
        test
        .groupby("recipe_id")
        .agg(
            test_sum=("rating", "sum"),
            test_count=("rating", "count"),
            test_average_rating=("rating", "mean")
        )
        .reset_index()
    )

    evaluation_table = recipe_stats.merge(
        test_stats,
        on="recipe_id",
        how="left"
    )

    test_columns = ["test_sum", "test_count", "test_average_rating"]
    evaluation_table[test_columns] = evaluation_table[test_columns].fillna(0)
    evaluation_table["test_count"] = (
        evaluation_table["test_count"].astype(int)
    )

    return evaluation_table


def evaluate_rankings(train, test, top_sizes=(100, 1000)):
    """
    Compare the two rankings using the test ratings.

    Both rankings are built on the train set only. Only recipes with
    at least one test rating are evaluated, then the top N of each
    ranking is selected and its mean test rating is calculated.

    Parameters
    ----------
    train : pandas.DataFrame
        Train set of valid ratings.
    test : pandas.DataFrame
        Test set of valid ratings.
    top_sizes : tuple of int, optional
        Sizes of the top lists to evaluate.

    Returns
    -------
    tuple
        A DataFrame with the mean test rating of each ranking and top
        size, and the baseline (mean test rating of all evaluated
        recipes).
    """
    evaluation = build_evaluation_table(train, test)

    # Rankings are built on all train recipes (no test information used)
    rankings = {
        "Simple average": simple_average_ranking(evaluation),
        "Bayesian average": bayesian_weighted_ranking(evaluation),
    }

    # Only recipes with test ratings can be evaluated
    rankings = {
        method: ranking[ranking["test_count"] > 0]
        for method, ranking in rankings.items()
    }

    results = []

    for top_n in top_sizes:
        for method, ranking in rankings.items():
            top = ranking.head(top_n)
            mean_test_rating = (
                top["test_sum"].sum() / top["test_count"].sum()
            )
            results.append({
                "method": method,
                "top_n": top_n,
                "mean_test_rating": mean_test_rating,
            })

    evaluable = evaluation[evaluation["test_count"] > 0]
    baseline = evaluable["test_sum"].sum() / evaluable["test_count"].sum()

    return pd.DataFrame(results), baseline


def compare_category_shares(ranking, category_column, top_n=100):
    """
    Compare the share of each category in the whole ranking and in its top.

    Parameters
    ----------
    ranking : pandas.DataFrame
        Ranking sorted from the best to the worst recipe, containing
        the column with the category of each recipe.
    category_column : str
        Name of the column containing the categories.
    top_n : int, optional
        Number of top recipes to consider.

    Returns
    -------
    pandas.DataFrame
        One row per category, with the percentage of recipes in the whole
        ranking (all_recipes) and in the top (top_recipes).

    Raises
    ------
    ValueError
        If the category column is missing or top_n is not positive.
    """

    if category_column not in ranking.columns:
        raise ValueError(f"Missing required column: '{category_column}'")

    if top_n <= 0:
        raise ValueError("top_n must be greater than zero.")

    all_shares = (
        ranking[category_column].value_counts(normalize=True) * 100
    )

    top_shares = (
        ranking.head(top_n)[category_column].value_counts(normalize=True)
        * 100
    )

    shares = pd.DataFrame({
        "all_recipes": all_shares,
        "top_recipes": top_shares
    })

    return shares.fillna(0)


def load_recipes_with_stats(recipe_columns=None, how="inner"):
    """
    Load the recipes and add their rating statistics.

    Only the columns recipe_id and rating are loaded from the
    interactions, to reduce memory usage.

    Parameters
    ----------
    recipe_columns : list, optional
        Recipe columns to load. If None, all columns are loaded.
        The column id is always required to link the two datasets.
    how : {"inner", "left"}, optional
        "inner" keeps only recipes with valid ratings, "left" keeps
        all recipes.

    Returns
    -------
    pandas.DataFrame
        Recipes with the columns recipe_id, rating_count
        and average_rating.

    Raises
    ------
    ValueError
        If how is not valid or the column id is not requested.
    """

    if how not in ("inner", "left"):
        raise ValueError("how must be 'inner' or 'left'.")

    if recipe_columns is not None and "id" not in recipe_columns:
        raise ValueError("recipe_columns must include 'id'.")

    recipes = load_recipes(usecols=recipe_columns)

    interactions = load_interactions(usecols=["recipe_id", "rating"])
    valid_interactions = filter_valid_interactions(interactions)
    recipe_stats = calculate_recipe_stats(valid_interactions)

    recipes_with_stats = recipes.merge(
        recipe_stats,
        left_on="id",
        right_on="recipe_id",
        how=how
    )

    # Sort by id so that ties in the rankings are always broken in the
    # same way, in the notebooks and in the app
    return recipes_with_stats.sort_values("id").reset_index(drop=True)
