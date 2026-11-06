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
        ascending=False
    ).copy()

    return ranking

