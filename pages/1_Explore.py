import streamlit as st
import pandas as pd

from recipe_project.data_loader import load_recipes, load_interactions
from recipe_project.cleaning import filter_valid_interactions
from recipe_project.analysis import calculate_recipe_stats


@st.cache_data
def get_recipe_data():
    """Load recipes and calculate their rating statistics."""

    recipes = load_recipes()
    interactions = load_interactions()

    valid_interactions = filter_valid_interactions(interactions)
    recipe_stats = calculate_recipe_stats(valid_interactions)

    recipes_with_stats = recipes.merge(
        recipe_stats,
        left_on="id",
        right_on="recipe_id",
        how="left"
    )

    return recipes_with_stats


# Load data
recipes = get_recipe_data()


# Page title
st.title("Explore Recipes")

st.write(
    "Search for recipes and explore their main characteristics."
)


# Recipe search
search_term = st.text_input("Search for a recipe")

# Recipe filters
st.subheader("Filter recipes")

col1, col2, col3 = st.columns(3)

with col1:
    max_minutes = st.selectbox(
        "⏱️ Maximum preparation time",
        [None, 15, 30, 45, 60, 90, 120],
        format_func=lambda x: (
            "Any duration" if x is None else f"Up to {x} minutes"
        )
    )

with col2:
    max_ingredients = st.selectbox(
        "🥕 Maximum number of ingredients",
        [None, 5, 10, 15, 20],
        format_func=lambda x: (
            "Any number" if x is None else f"Up to {x} ingredients"
        )
    )

with col3:
    min_rating = st.selectbox(
        "⭐ Minimum avergae rating",
        [0, 1, 2, 3, 4, 5],
        format_func=lambda x: (
            "Any rating" if x == 0 else f"{x}+ stars"
        )
    )


# Filter recipes by name
filtered_recipes = recipes

if search_term:
    normalized_names = (
        recipes["name"]
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    normalized_search = " ".join(search_term.split())

    filtered_recipes = recipes[
        normalized_names.str.contains(
            normalized_search,
            case=False,
            na=False,
            regex=False
        )
    ]

# Apply recipe filters
if max_minutes is not None:
    filtered_recipes = filtered_recipes[
        filtered_recipes["minutes"] <= max_minutes
    ]

if max_ingredients is not None:
    filtered_recipes = filtered_recipes[
        filtered_recipes["n_ingredients"] <= max_ingredients
    ]

filtered_recipes = filtered_recipes[
    filtered_recipes["average_rating"].fillna(0) >= min_rating
]

# Display results
st.write(f"Recipes found: {len(filtered_recipes):,}")

st.caption("Showing up to 20 recipes.")

for _, recipe in filtered_recipes.head(20).iterrows():

    with st.container(border=True):

        # Recipe name
        st.subheader(f"🍽️ {recipe['name']}")

        # Rating information
        col1, col2 = st.columns([2, 1])

        with col1:
            if pd.notna(recipe["average_rating"]):

                average_rating = recipe["average_rating"]
                rating_count = int(recipe["rating_count"])

                full_stars = int(round(average_rating))
                stars = "★" * full_stars + "☆" * (5 - full_stars)

                st.markdown(
                    f"**:orange[{stars}]**  {average_rating:.2f}/5"
                )

                st.caption(f"⭐ {rating_count:,} ratings")

            else:
                st.write("No ratings available.")

        with col2:
            if pd.notna(recipe["minutes"]) and recipe["minutes"] > 0:
                st.write(f"⏱️ {recipe['minutes']} min")
                st.caption("Preparation time")
            else:
                st.write("⏱️ Not available")
                st.caption("Preparation time")
        
        # Number of ingredients
        st.write(
           f"🥕 {recipe['n_ingredients']} ingredients"
        )

        # Recipe description
        if pd.notna(recipe["description"]) and recipe["description"].strip():
            with st.expander("📝 View description"):
                st.write(recipe["description"])

