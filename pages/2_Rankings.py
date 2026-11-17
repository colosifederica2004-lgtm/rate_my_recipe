import streamlit as st

from recipe_project.data_loader import load_recipes, load_interactions
from recipe_project.cleaning import filter_valid_interactions
from recipe_project.analysis import calculate_recipe_stats
from recipe_project.plots import ranking_comparison
from recipe_project.ranking import (
    simple_average_ranking,
    bayesian_weighted_ranking
)

# Page title
st.title("🏆 Recipe Rankings")

st.write(
    """
    Discover the highest-rated recipes and compare two ranking methods:
    Simple Average Ranking and Bayesian Weighted Ranking.
    """
)

st.divider()

@st.cache_data
def load_ranking_data():
    """Load and prepare data for recipe rankings."""

    recipes = load_recipes()
    interactions = load_interactions()

    valid_interactions = filter_valid_interactions(interactions)
    recipe_stats = calculate_recipe_stats(valid_interactions)

    recipes_with_stats = recipes.merge(
        recipe_stats,
        left_on="id",
        right_on="recipe_id",
        how="inner"
    )

    return recipes_with_stats

# Load ranking data
recipes_with_stats = load_ranking_data()

# Calculate rankings
simple_ranking = simple_average_ranking(recipes_with_stats)

bayesian_ranking = bayesian_weighted_ranking(recipes_with_stats)

# Ranking display options
st.subheader("Explore the Rankings")

top_n = st.selectbox(
    "Number of recipes to display",
    [10, 20, 50, 100],
    index=1
)


# Ranking results
st.divider()
st.subheader("Ranking Results")

col1, col2 = st.columns(2)

# Simple Average Ranking
with col1:
    st.markdown("### ⭐ Simple Average")

    simple_top = simple_ranking.head(top_n)

    for position, (_, recipe) in enumerate(simple_top.iterrows(), start=1):

        with st.container(border=True):
            st.markdown(f"**#{position} – {recipe['name']}**")

            st.write(
                f"⭐ Average rating: {recipe['average_rating']:.2f}/5"
            )

            st.write(
                f"👥 Number of ratings: {recipe['rating_count']:,}"
            )


# Bayesian Weighted Ranking
with col2:
    st.markdown("### 🏆 Bayesian Weighted")

    bayesian_top = bayesian_ranking.head(top_n)

    for position, (_, recipe) in enumerate(bayesian_top.iterrows(), start=1):

        with st.container(border=True):
            st.markdown(f"**#{position} – {recipe['name']}**")

            st.write(
                f"🏆 Bayesian score: {recipe['bayesian_score']:.3f}"
            )

            st.write(
                f"👥 Number of ratings: {recipe['rating_count']:,}"
            )

            st.caption(
                f"Original average rating: {recipe['average_rating']:.2f}/5"
            )