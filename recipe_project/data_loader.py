"""Functions to load the Food.com datasets from CSV files."""

from pathlib import Path

import pandas as pd

# The project folder is the parent of the folder that contains this file.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

RECIPES_FILE = "RAW_recipes.csv"
INTERACTIONS_FILE = "RAW_interactions.csv"

# Columns that every file must contain for the analysis to work.
REQUIRED_COLUMNS = {
    RECIPES_FILE: {"id", "name", "minutes", "tags", "n_ingredients"},
    INTERACTIONS_FILE: {"user_id", "recipe_id", "date", "rating", "review"},
}


def load_csv(file_name, data_dir=DATA_DIR):
    """
    Load a CSV file from the data folder and check its columns.

    Parameters
    ----------
    file_name : str
        Name of the CSV file, for example "RAW_recipes.csv".
    data_dir : Path or str, optional
        Folder that contains the file. By default, the data/ folder
        of the project.

    Returns
    -------
    pandas.DataFrame
        The content of the file.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file cannot be read as a CSV or if required columns
        are missing.
    """
    path = Path(data_dir) / file_name

    try:
        data = pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"File not found: {path}. Download the dataset from Kaggle "
            "and save it in the data/ folder (see the README)."
        ) from None
    except (pd.errors.EmptyDataError, pd.errors.ParserError) as error:
        raise ValueError(f"{file_name} cannot be read as a CSV: {error}") from error

    missing = REQUIRED_COLUMNS.get(file_name, set()) - set(data.columns)
    if missing:
        raise ValueError(f"{file_name} is missing columns: {sorted(missing)}")

    return data


def load_recipes(data_dir=DATA_DIR):
    """Load the recipes table (RAW_recipes.csv)."""
    return load_csv(RECIPES_FILE, data_dir)


def load_interactions(data_dir=DATA_DIR):
    """Load the interactions table (RAW_interactions.csv)."""
    return load_csv(INTERACTIONS_FILE, data_dir)