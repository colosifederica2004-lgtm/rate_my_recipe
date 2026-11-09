"""Functions to clean and prepare the Food.com datasets for analysis."""

import pandas as pd

def filter_valid_interactions(interactions):
    """
    Keep interactions with valid recipe IDs and ratings from 1 to 5.

    Ratings equal to zero are excluded from the ranking dataset,
    but are counted separately for data quality analysis.

    Parameters
    ----------
    interactions : pandas.DataFrame
        Original interactions dataset.

    Returns
    -------
    pandas.DataFrame
        Cleaned interactions containing valid ratings.

    Raises
    ------
    ValueError
        If required columns are missing.
    """

    required_columns = {"recipe_id", "rating"}

    missing_columns = required_columns - set(interactions.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    cleaned = interactions.copy()

    # Convert ratings to numeric values
    cleaned["rating"] = pd.to_numeric(
        cleaned["rating"],
        errors="coerce"
    )

    # Remove rows without a recipe ID or a valid numeric rating
    cleaned = cleaned.dropna(
        subset=["recipe_id", "rating"]
    )

    # Keep only integer ratings between 1 and 5
    valid_mask = cleaned["rating"].isin([1, 2, 3, 4, 5])

    valid_interactions = cleaned.loc[valid_mask].copy()

    # Store ratings as integers
    valid_interactions["rating"] = (
        valid_interactions["rating"].astype("int8")
    )

    return valid_interactions.reset_index(drop=True)


def get_interaction_quality_report(interactions):
    """
    Generate a report describing the quality of the original data.

    No rows are removed by this function.

    Returns
    -------
    pandas.Series
        Counts of missing values, invalid ratings and duplicates.
    """

    required_columns = {"recipe_id", "rating"}

    missing_columns = required_columns - set(interactions.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    numeric_ratings = pd.to_numeric(
        interactions["rating"],
        errors="coerce"
    )

    report = {
        "total_interactions": len(interactions),
        "missing_recipe_id": int(
            interactions["recipe_id"].isna().sum()
        ),
        "missing_rating": int(
            interactions["rating"].isna().sum()
        ),
        "non_numeric_ratings": int(
            (interactions["rating"].notna() &
             numeric_ratings.isna()).sum()
        ),
        "zero_ratings": int(
            (numeric_ratings == 0).sum()
        ),
        "ratings_outside_0_5": int(
            (~numeric_ratings.isin([0, 1, 2, 3, 4, 5]) &
             numeric_ratings.notna()).sum()
        ),
        "exact_duplicate_rows": int(
            interactions.duplicated().sum()
        )
    }

    return pd.Series(report, name="Value")
