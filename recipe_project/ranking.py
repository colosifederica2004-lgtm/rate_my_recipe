"""Functions to calculate and compare recipe rankings."""

import pandas as pd

# simple average ranking 
def simple_average_ranking(recipe_stats):
    """
    Rank recipes according to their average rating.

    Parameters
    ----------
    recipe_stats : pandas.DataFrame
        DataFrame containing recipe-level statistics.

    Returns
    -------
    pandas.DataFrame
        Recipes sorted from the highest to the lowest average rating.
    """
    ranking = recipe_stats.sort_values(
        by="average_rating",
        ascending=False,
        kind = "stable"
    ).copy()

    return ranking



# Bayesian Weighted Ranking

def bayesian_weighted_ranking(recipe_stats, m=None):
    """
    Rank recipes using the Bayesian weighted rating formula.

    Parameters
    ----------
    recipe_stats : pandas.DataFrame
        DataFrame containing recipe-level statistics.
    m : float, optional
        Weight of the overall average rating. If None, it is the 90th
        percentile of rating_count.

    Returns
    -------
    pandas.DataFrame
        Recipes sorted by Bayesian weighted score.
    """
    ranking = recipe_stats.copy()

    if m is None:
        m = recipe_stats["rating_count"].quantile(0.90)

    if m <= 0:
        raise ValueError("m must be greater than zero.")

    C = (
    (recipe_stats["average_rating"] * recipe_stats["rating_count"]).sum()
    / recipe_stats["rating_count"].sum()
    )
    v = recipe_stats["rating_count"]
    R = recipe_stats["average_rating"]

    ranking["bayesian_score"] = (
        (v / (v + m)) * R +
        (m / (v + m)) * C
    )

    ranking = ranking.sort_values(
        by="bayesian_score",
        ascending=False,
        kind = "stable"
    )

    return ranking

