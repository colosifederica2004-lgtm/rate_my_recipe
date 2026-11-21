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


MAX_PREPARATION_MINUTES = 1000


def filter_valid_preparation_times(recipes):
    """
    Keep recipes with a preparation time between 1 and 1000 minutes.

    Recipes with zero minutes or more than 1000 minutes are excluded
    from the preparation time analysis. The threshold is an operational
    choice to limit the influence of extreme values.

    Parameters
    ----------
    recipes : pandas.DataFrame
        Recipes dataset containing the column minutes.

    Returns
    -------
    pandas.DataFrame
        A filtered copy of the recipes.

    Raises
    ------
    ValueError
        If the column minutes is missing.
    """

    if "minutes" not in recipes.columns:
        raise ValueError("Missing required column: 'minutes'")

    valid_mask = (
        (recipes["minutes"] > 0)
        & (recipes["minutes"] <= MAX_PREPARATION_MINUTES)
    )

    return recipes.loc[valid_mask].copy()


def add_preparation_category(recipes):
    """
    Add the column preparation_category to the recipes.

    Categories: Quick (up to 30 minutes), Medium (31-60),
    Long (61-90) and Very Long (over 90).

    Parameters
    ----------
    recipes : pandas.DataFrame
        Recipes dataset containing the column minutes.

    Returns
    -------
    pandas.DataFrame
        A copy of the recipes with the new column.

    Raises
    ------
    ValueError
        If the column minutes is missing.
    """

    if "minutes" not in recipes.columns:
        raise ValueError("Missing required column: 'minutes'")

    preparation_categories = []

    for minutes in recipes["minutes"]:
        if pd.isna(minutes) or minutes < 0:
            preparation_categories.append("Unknown")
        elif minutes <= 30:
            preparation_categories.append("Quick")
        elif minutes <= 60:
            preparation_categories.append("Medium")
        elif minutes <= 90:
            preparation_categories.append("Long")
        else:
            preparation_categories.append("Very Long")

    result = recipes.copy()
    result["preparation_category"] = preparation_categories

    return result


def add_ingredient_category(recipes):
    """
    Add the column ingredient_category to the recipes.

    Categories: Few Ingredients (1-4), Medium Ingredients (5-10)
    and Many Ingredients (over 10).

    Parameters
    ----------
    recipes : pandas.DataFrame
        Recipes dataset containing the column n_ingredients.

    Returns
    -------
    pandas.DataFrame
        A copy of the recipes with the new column.

    Raises
    ------
    ValueError
        If the column n_ingredients is missing.
    """

    if "n_ingredients" not in recipes.columns:
        raise ValueError("Missing required column: 'n_ingredients'")

    ingredient_categories = []

    for n in recipes["n_ingredients"]:
        if n <= 4:
            ingredient_categories.append("Few Ingredients")
        elif n <= 10:
            ingredient_categories.append("Medium Ingredients")
        else:
            ingredient_categories.append("Many Ingredients")

    result = recipes.copy()
    result["ingredient_category"] = ingredient_categories

    return result
