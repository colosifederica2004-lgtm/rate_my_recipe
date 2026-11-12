"""Functions to calculate and compare recipe rankings."""

import pandas as pd

def _validate_recipe_stats(recipe_stats):
    """Validate the input DataFrame for ranking calculations."""

    if not isinstance(recipe_stats, pd.DataFrame):
        raise TypeError("recipe_stats must be a pandas DataFrame.")

    if recipe_stats.empty:
        raise ValueError("recipe_stats cannot be empty.")

    required_columns = {"average_rating", "rating_count"}

    missing_columns = required_columns - set(recipe_stats.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    if recipe_stats[list(required_columns)].isna().any().any():
        raise ValueError("Ranking columns cannot contain missing values.")

    if not pd.api.types.is_numeric_dtype(recipe_stats["average_rating"]):
        raise ValueError("average_rating must be numeric.")

    if not pd.api.types.is_numeric_dtype(recipe_stats["rating_count"]):
        raise ValueError("rating_count must be numeric.")

    if not recipe_stats["average_rating"].between(1, 5).all():
        raise ValueError("average_rating must be between 1 and 5.")

    if (recipe_stats["rating_count"] <= 0).any():
        raise ValueError("rating_count must be greater than zero.")


# --------------------------------------------------
# 1. SIMPLE AVERAGE RANKING
# --------------------------------------------------
 
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
    _validate_recipe_stats(recipe_stats)

    ranking = recipe_stats.copy()

    return ranking.sort_values(
        by="average_rating",
        ascending=False,
        kind="stable"
    )

# --------------------------------------------------
# 2. BAYESIAN WEIGHTED RANKING
# --------------------------------------------------

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
    _validate_recipe_stats(recipe_stats)

    ranking = recipe_stats.copy()


    # Determine the regularization parameter
    if m is None:
        m = recipe_stats["rating_count"].quantile(0.90)

    if (
        isinstance(m, bool)
        or not isinstance(m, (int, float))
        or not pd.notna(m)
        or m <= 0
        or m == float("inf")
    ):
        raise ValueError("m must be a finite positive number.")

    
    # Calculate the global weighted average rating
    C = (
        ranking["average_rating"] * ranking["rating_count"]
    ).sum() / ranking["rating_count"].sum()

    # Number of reviews and average rating for each recipe
    v = ranking["rating_count"]
    R = ranking["average_rating"]

    # Bayesian weighted score
    ranking["bayesian_score"] = (
        (v / (v + m)) * R +
        (m / (v + m)) * C
    )

    return ranking.sort_values(
        by="bayesian_score",
        ascending=False,
        kind="stable"
    )

