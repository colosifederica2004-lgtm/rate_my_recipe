"""Functions to analyse recipe ratings and calculate recipe-level statistics."""

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
        A DataFrame with one row per recipe and two columns:
        rating_count and average_rating.
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