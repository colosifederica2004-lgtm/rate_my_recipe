
import streamlit as st
import pandas as pd
import plotly.express as px

from recipe_project.data_loader import load_recipes, load_interactions
from recipe_project.cleaning import filter_valid_interactions
from recipe_project.analysis import calculate_recipe_stats
from recipe_project.ranking import bayesian_weighted_ranking


st.set_page_config(
    page_title="Recipe Characteristics",
    page_icon="🥕",
    layout="wide"
)


st.title("🥕 Recipe Characteristics")

st.write(
    "Explore how preparation time and number of ingredients "
    "are represented in the Bayesian Weighted Ranking."
)

st.divider()


@st.cache_data
def load_characteristics_data():
    """Load and prepare data for recipe characteristics analysis."""

    # Load datasets
    recipes = load_recipes()
    interactions = load_interactions()

    # Clean interactions
    valid_interactions = filter_valid_interactions(interactions)

    # Calculate recipe-level statistics
    recipe_stats = calculate_recipe_stats(valid_interactions)

    # Combine recipe information and rating statistics
    recipes_with_stats = recipes.merge(
        recipe_stats,
        left_on="id",
        right_on="recipe_id",
        how="inner"
    )

    # Calculate Bayesian ranking
    bayesian_ranking = bayesian_weighted_ranking(recipes_with_stats)

    # Select the top 100 recipes
    bayesian_top_100 = bayesian_ranking.head(100)

    return recipes_with_stats, bayesian_top_100


# Load prepared data
recipes_with_stats, bayesian_top_100 = load_characteristics_data()


# --------------------------------------------------
# PREPARATION TIME ANALYSIS
# --------------------------------------------------

st.header("1. Preparation Time Analysis")

st.write(
    "Compare the preparation time distribution of all rated recipes "
    "with the distribution of the 100 highest-ranked recipes."
)


# Define preparation time categories
categories = ["Quick", "Medium", "Long", "Very Long"]


# Filter recipes with valid preparation times
recipes_time = recipes_with_stats[
    (recipes_with_stats["minutes"] > 0) &
    (recipes_with_stats["minutes"] <= 1000)
].copy()


# Assign preparation time categories to all rated recipes
preparation_categories = []

for minutes in recipes_time["minutes"]:

    if minutes <= 30:
        preparation_categories.append("Quick")

    elif minutes <= 60:
        preparation_categories.append("Medium")

    elif minutes <= 90:
        preparation_categories.append("Long")

    else:
        preparation_categories.append("Very Long")


recipes_time["preparation_category"] = preparation_categories


# Calculate distribution for all rated recipes
all_recipes_distribution = (
    recipes_time["preparation_category"]
    .value_counts()
    .reindex(categories, fill_value=0)
)

all_recipes_percentages = (
    all_recipes_distribution / len(recipes_time) * 100
)


# Filter Bayesian Top 100 by valid preparation times
bayesian_top_100_time = bayesian_top_100[
    (bayesian_top_100["minutes"] > 0) &
    (bayesian_top_100["minutes"] <= 1000)
].copy()


# Assign preparation time categories to Bayesian Top 100
top_100_categories = []

for minutes in bayesian_top_100_time["minutes"]:

    if minutes <= 30:
        top_100_categories.append("Quick")

    elif minutes <= 60:
        top_100_categories.append("Medium")

    elif minutes <= 90:
        top_100_categories.append("Long")

    else:
        top_100_categories.append("Very Long")


bayesian_top_100_time["preparation_category"] = top_100_categories


# Calculate distribution for Bayesian Top 100
top_100_distribution = (
    bayesian_top_100_time["preparation_category"]
    .value_counts()
    .reindex(categories, fill_value=0)
)

top_100_percentages = (
    top_100_distribution / len(bayesian_top_100_time) * 100
)


# --------------------------------------------------
# PREPARATION TIME COMPARISON CHART
# --------------------------------------------------

preparation_comparison = pd.DataFrame({
    "Category": categories * 2,
    "Group": (
        ["All Rated Recipes"] * len(categories)
        + ["Bayesian Top 100"] * len(categories)
    ),
    "Percentage": (
        all_recipes_percentages.tolist()
        + top_100_percentages.tolist()
    )
})


fig = px.bar(
    preparation_comparison,
    x="Category",
    y="Percentage",
    color="Group",
    barmode="group",
    category_orders={"Category": categories},
    color_discrete_map={
        "All Rated Recipes": "#E75480",
        "Bayesian Top 100": "#7B2CBF"
    },
    labels={
        "Category": "Preparation Time",
        "Percentage": "Recipes (%)",
        "Group": "Recipe Group"
    },
    title="Preparation Time Distribution"
)

fig.update_layout(
    template="plotly_white",
    height=450,
    yaxis_title="Percentage of Recipes (%)",
    xaxis_title="Preparation Time Category",
    legend_title="",
)

st.plotly_chart(fig, width="stretch")


# --------------------------------------------------
# PREPARATION TIME INTERPRETATION
# --------------------------------------------------

st.subheader("Key Observations")

st.markdown(
    """
    - **Quick:** almost identical representation in both groups
      (43.00% vs. 43.06%).
    - **Medium:** less represented in the Bayesian Top 100
      (26.00% vs. 30.66%).
    - **Long and Very Long:** more represented in the Bayesian Top 100
      (16.00% and 15.00% vs. 12.69% and 13.58%).
    """
)

st.caption(
    "These results describe differences in category representation "
    "and do not establish a causal relationship between preparation "
    "time and recipe ranking."
)


# --------------------------------------------------
# INGREDIENT ANALYSIS
# --------------------------------------------------

st.divider()

st.header("2. Ingredient Analysis")

st.write(
    "Investigate whether the number of ingredients is related "
    "to recipe ratings and ranking positions, and examine how "
    "recipes with different numbers of ingredients are represented "
    "in the Bayesian Weighted Ranking."
)

# Define ingredient categories
ingredient_categories = ["Few", "Medium", "Many"]


# Assign ingredient categories to all rated recipes
ingredient_groups = []

for ingredients in recipes_with_stats["n_ingredients"]:

    if ingredients <= 4:
        ingredient_groups.append("Few")

    elif ingredients <= 10:
        ingredient_groups.append("Medium")

    else:
        ingredient_groups.append("Many")


recipes_with_stats["ingredient_category"] = ingredient_groups

# Assign ingredient categories to the Bayesian Top 100
bayesian_top_100 = bayesian_top_100.copy()

top_100_ingredient_groups = []

for ingredients in bayesian_top_100["n_ingredients"]:

    if ingredients <= 4:
        top_100_ingredient_groups.append("Few")

    elif ingredients <= 10:
        top_100_ingredient_groups.append("Medium")

    else:
        top_100_ingredient_groups.append("Many")


bayesian_top_100["ingredient_category"] = top_100_ingredient_groups

# Ingredient distribution across all rated recipes
all_ingredients_distribution = (
    recipes_with_stats["ingredient_category"]
    .value_counts()
    .reindex(ingredient_categories, fill_value=0)
)

all_ingredients_percentages = (
    all_ingredients_distribution / len(recipes_with_stats) * 100
)


# Ingredient distribution in the Bayesian Top 100
top_100_ingredients_distribution = (
    bayesian_top_100["ingredient_category"]
    .value_counts()
    .reindex(ingredient_categories, fill_value=0)
)

top_100_ingredients_percentages = (
    top_100_ingredients_distribution / len(bayesian_top_100) * 100
)


# Display results
print("All rated recipes:")
print(all_ingredients_percentages.round(2))

print("\nBayesian Top 100:")
print(top_100_ingredients_percentages.round(2))

# Create comparison DataFrame
ingredient_comparison = pd.DataFrame({
    "Category": ingredient_categories * 2,
    "Group": (
        ["All Rated Recipes"] * len(ingredient_categories)
        + ["Bayesian Top 100"] * len(ingredient_categories)
    ),
    "Percentage": (
        all_ingredients_percentages.tolist()
        + top_100_ingredients_percentages.tolist()
    )
})


# Create chart
fig = px.bar(
    ingredient_comparison,
    x="Category",
    y="Percentage",
    color="Group",
    barmode="group",
    category_orders={"Category": ingredient_categories},
    color_discrete_map={
        "All Rated Recipes": "#E75480",
        "Bayesian Top 100": "#7B2CBF"
    },
    labels={
        "Category": "Number of Ingredients",
        "Percentage": "Recipes (%)",
        "Group": "Recipe Group"
    },
    title="Number of Ingredients Distribution"
)

fig.update_layout(
    template="plotly_white",
    height=450,
    yaxis_title="Percentage of Recipes (%)",
    xaxis_title="Ingredient Category",
    legend_title=""
)

st.plotly_chart(fig, width="stretch")

# observations
st.subheader("Key Observations")

st.markdown(
    """
    - **Few:** overrepresented in the Bayesian Top 100 (22% vs. 9.33%).
    - **Medium:** less represented (49% vs. 59.27%).
    - **Many:** slightly less represented (29% vs. 31.40%).
    """
)

st.caption(
    "These results describe differences in category representation "
    "and do not establish a causal relationship between the number "
    "of ingredients and recipe ranking."
)