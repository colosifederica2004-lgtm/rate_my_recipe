"""Rankings page: compare the Simple Average and Bayesian rankings."""

import streamlit as st

from recipe_project.analysis import load_recipes_with_stats
from recipe_project.ranking import (
    simple_average_ranking,
    bayesian_weighted_ranking
)


@st.cache_data
def load_ranking_data():
    """Load recipes with their rating statistics."""

    return load_recipes_with_stats(recipe_columns=["id", "name"])


# Load ranking data
recipes_with_stats = load_ranking_data()

# Calculate rankings
simple_ranking = simple_average_ranking(recipes_with_stats)

bayesian_ranking = bayesian_weighted_ranking(recipes_with_stats)

# Page title
st.title("Recipe Rankings")

st.write(
    """
    Discover the highest-rated recipes and compare two ranking methods:
    Simple Average Ranking and Bayesian Weighted Ranking.
    """
)

st.divider()

# Ranking display options
top_n = st.selectbox(
    "Number of recipes to display",
    [10, 20, 50, 100],
    index=1
)

# Ranking results
col1, col2 = st.columns(2)

# Simple Average Ranking
with col1:
    st.markdown("### ⭐ Simple Average")
    st.caption("Ordered by average rating only.")

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
    st.caption(
        "Ordered by Bayesian score, which also takes "
        "the number of ratings into account."
    )

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
