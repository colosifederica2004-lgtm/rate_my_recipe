"""Functions to clean and prepare the Food.com datasets for analysis."""

import pandas as pd

def filter_valid_interactions(interactions):
    """
    Keep only interactions with valid numerical ratings (1 to 5).
    """
    valid_interactions = interactions[
        interactions["rating"].between(1, 5)
    ].copy()

    return valid_interactions