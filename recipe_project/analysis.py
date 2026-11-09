"""Functions to analyse recipe ratings and calculate recipe-level statistics."""

import numpy as np
import pandas as pd

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
DEFAULT_SEED = 42

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
    if not 0 < train_fraction < 1:
        raise ValueError("train_fraction must be between 0 and 1")

    rng = np.random.default_rng(seed)
    is_train = rng.random(len(interactions)) < train_fraction

    return interactions[is_train].copy(), interactions[~is_train].copy()


def build_evaluation_table(train, test):
    """
    Combine the train statistics with the test ratings of each recipe.

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
    train_stats = calculate_recipe_stats(train)

    test_stats = (
        test.groupby("recipe_id")["rating"]
        .agg(test_sum="sum", test_count="count")
        .reset_index()
    )

    evaluation = train_stats.merge(test_stats, on="recipe_id", how="left")
    evaluation[["test_sum", "test_count"]] = (
        evaluation[["test_sum", "test_count"]].fillna(0)
    )

    return evaluation