
import streamlit as st

from recipe_project.data_loader import load_recipes, load_interactions
from recipe_project.cleaning import filter_valid_interactions
from recipe_project.analysis import calculate_recipe_stats

st.set_page_config(
    page_title="Rate My Recipe",
    page_icon="🍽️",
    layout="wide",
)

@st.cache_data
def load_project_data():
    """Load and prepare the recipe and interaction datasets."""

    recipes = load_recipes()
    interactions = load_interactions()

    valid_interactions = filter_valid_interactions(interactions)
    recipe_stats = calculate_recipe_stats(valid_interactions)

    return recipes, valid_interactions, recipe_stats


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

st.title("🍽️ Rate My Recipe")

st.markdown(
    """
    ### Discover recipes. Explore ratings. Find the best recipes.

    Welcome to **Rate My Recipe**, a data-driven project that explores
    how users rate recipes and how different ranking methods can
    influence the results.
    """
)

st.divider()

recipes, valid_interactions, recipe_stats = load_project_data()

st.subheader("The Dataset at a Glance")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Recipes", f"{len(recipes):,}")

with col2:
    st.metric("Valid Ratings", f"{len(valid_interactions):,}")

with col3:
    st.metric("Recipes with Ratings", f"{len(recipe_stats):,}")

st.divider()

st.subheader("Explore Rate My Recipe")

st.markdown(
    """
    Use the sections in the sidebar to discover the project:

    - **Explore:** search recipes and investigate their characteristics.
    - **Rankings:** compare Simple Average and Bayesian Weighted rankings.
    - **Analysis:** explore patterns in ratings, preparation times,
      and number of ingredients.
    """
)
