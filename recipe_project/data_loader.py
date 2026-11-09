
"""Functions to load the Food.com datasets from CSV files."""

from pathlib import Path

import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

RECIPES_FILE = "RAW_recipes.csv"
INTERACTIONS_FILE = "RAW_interactions.csv"


# Required columns for each dataset
REQUIRED_COLUMNS = {
    RECIPES_FILE: {
        "id",
        "name",
        "minutes",
        "tags",
        "n_ingredients",
    },
    INTERACTIONS_FILE: {
        "user_id",
        "recipe_id",
        "date",
        "rating",
        "review",
    },
}


def load_csv(file_name, data_dir=DATA_DIR, usecols=None):
    """
    Load a Food.com CSV dataset and validate its structure.

    Parameters
    ----------
    file_name : str
        Name of the CSV file.
    data_dir : Path or str, optional
        Directory containing the dataset.
    usecols : list, optional
        Columns to load. If None, all columns are loaded.

    Returns
    -------
    pandas.DataFrame
        Loaded dataset.

    Raises
    ------
    ValueError
        If the filename is unsupported or the dataset is invalid.
    FileNotFoundError
        If the file does not exist.
    """

    if file_name not in REQUIRED_COLUMNS:
        raise ValueError(
            f"Unsupported dataset: {file_name}. "
            f"Available datasets: {list(REQUIRED_COLUMNS)}"
        )

    path = Path(data_dir) / file_name

    if not path.is_file():
        raise FileNotFoundError(
            f"Dataset not found: {path}\n"
            "Download the Food.com datasets and place them "
            "inside the data/ folder."
        )

    try:
        # Read the header first to validate the dataset structure
        header = pd.read_csv(
            path,
            nrows=0,
            encoding="utf-8-sig"
        )

        available_columns = set(header.columns)

        missing_columns = (
            REQUIRED_COLUMNS[file_name] - available_columns
        )

        if missing_columns:
            raise ValueError(
                f"{file_name} is missing required columns: "
                f"{sorted(missing_columns)}"
            )

        # Validate requested columns
        if usecols is not None:
            missing_requested = set(usecols) - available_columns

            if missing_requested:
                raise ValueError(
                    f"Requested columns not found: "
                    f"{sorted(missing_requested)}"
                )

        # Load the actual dataset
        data = pd.read_csv(
            path,
            usecols=usecols,
            encoding="utf-8-sig",
            low_memory=False
        )

    except (pd.errors.ParserError, pd.errors.EmptyDataError,
            UnicodeDecodeError, OSError) as error:

        raise ValueError(
            f"Unable to read {file_name}: {error}"
        ) from error

    # Check for duplicate column names
    if data.columns.duplicated().any():
        raise ValueError(
            f"{file_name} contains duplicate column names."
        )

    return data


def load_recipes(data_dir=DATA_DIR, usecols=None):
    """Load the RAW_recipes.csv dataset."""

    return load_csv(
        RECIPES_FILE,
        data_dir=data_dir,
        usecols=usecols
    )


def load_interactions(data_dir=DATA_DIR, usecols=None):
    """Load the RAW_interactions.csv dataset."""

    return load_csv(
        INTERACTIONS_FILE,
        data_dir=data_dir,
        usecols=usecols
    )
