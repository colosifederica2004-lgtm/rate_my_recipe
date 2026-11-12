"""Functions to analyse recipe ratings and calculate recipe-level statistics."""

import numpy as np
import pandas as pd

DEFAULT_SEED = 42

# Validate the cleaned interactions dataset before performing the analysis.
def _validate_interactions(interactions):
    """
    Validate the structure and contents of an interactions DataFrame.
    """

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
    """
    Build a table containing training statistics and test information
    for recipes present in both the training and test sets.

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
        how="inner"
    )

    evaluation_table["test_count"] = (
        evaluation_table["test_count"].astype(int)
    )

    return evaluation_table