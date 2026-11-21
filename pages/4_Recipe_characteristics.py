"""Recipe characteristics page: time and ingredients in the Bayesian top."""

import streamlit as st
import plotly.express as px

from recipe_project.analysis import (
    compare_category_shares,
    load_recipes_with_stats
)
from recipe_project.cleaning import (
    add_ingredient_category,
    add_preparation_category,
    filter_valid_preparation_times
)
from recipe_project.ranking import bayesian_weighted_ranking

TOP_N = 100

TIME_CATEGORIES = ["Quick", "Medium", "Long", "Very Long"]
INGREDIENT_CATEGORIES = [
    "Few Ingredients", "Medium Ingredients", "Many Ingredients"
]

GROUP_NAMES = {
    "all_recipes": "All Rated Recipes",
    "top_recipes": "Bayesian Top 100"
}


@st.cache_data
def load_characteristics_data():
    """Compare category shares in all recipes and in the Bayesian top."""

    recipes_with_stats = load_recipes_with_stats(
        recipe_columns=["id", "name", "minutes", "n_ingredients"]
    )

    ranking = bayesian_weighted_ranking(recipes_with_stats)

    # Preparation time: only recipes with a valid preparation time
    time_ranking = add_preparation_category(
        filter_valid_preparation_times(ranking)
    )

    time_shares = compare_category_shares(
        time_ranking, "preparation_category", top_n=TOP_N
    )

    # Number of ingredients
    ingredient_ranking = add_ingredient_category(ranking)

    ingredient_shares = compare_category_shares(
        ingredient_ranking, "ingredient_category", top_n=TOP_N
    )

    return time_shares, ingredient_shares


def make_bar_chart(shares, categories, title, xaxis_title):
    """Create a grouped bar chart from a table of category shares."""

    data = shares.reindex(categories).rename_axis("Category").reset_index()

    data = data.melt(
        id_vars="Category",
        var_name="Group",
        value_name="Percentage"
    )
    data["Group"] = data["Group"].map(GROUP_NAMES)

    fig = px.bar(
        data,
        x="Category",
        y="Percentage",
        color="Group",
        barmode="group",
        text_auto=".1f",
        category_orders={"Category": categories},
        color_discrete_map={
            "All Rated Recipes": "#E75480",
            "Bayesian Top 100": "#7B2CBF"
        },
        title=title
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
        template="plotly_white",
        height=450,
        yaxis_title="Percentage of Recipes (%)",
        xaxis_title=xaxis_title,
        legend_title=""
    )

    return fig


time_shares, ingredient_shares = load_characteristics_data()


st.title("Recipe Characteristics")

st.write(
    "Explore how preparation time and number of ingredients "
    "are represented in the Bayesian Weighted Ranking."
)

st.divider()

# --------------------------------------------------
# PREPARATION TIME ANALYSIS
# --------------------------------------------------

st.header("1. Preparation Time Analysis")

st.write(
    "Compare the preparation time distribution of all rated recipes "
    "with the distribution of the 100 highest-ranked recipes."
)

st.caption(
    "Quick: up to 30 minutes. Medium: 31 to 60. Long: 61 to 90. "
    "Very Long: more than 90 minutes. Recipes with a missing or "
    "unrealistic time (0 or over 1,000 minutes) are excluded."
)

st.plotly_chart(
    make_bar_chart(
        time_shares,
        TIME_CATEGORIES,
        "Preparation Time Distribution",
        "Preparation Time Category"
    ),
    width="stretch"
)

st.subheader("Key Observations")

st.markdown(
    """
    - **Quick:** almost identical representation in both groups
      (43.00% vs. 43.06%).
    - **Medium:** less represented in the Bayesian Top 100
      (25.00% vs. 30.66%).
    - **Long and Very Long:** more represented in the Bayesian Top 100
      (16.00% and 16.00% vs. 12.69% and 13.58%).
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
    "Investigate how recipes with different numbers of ingredients "
    "are represented in the Bayesian Weighted Ranking."
)

st.caption(
    "Few Ingredients: up to 4. Medium Ingredients: 5 to 10. "
    "Many Ingredients: more than 10."
)

st.plotly_chart(
    make_bar_chart(
        ingredient_shares,
        INGREDIENT_CATEGORIES,
        "Number of Ingredients Distribution",
        "Ingredient Category"
    ),
    width="stretch"
)

st.subheader("Key Observations")

st.markdown(
    """
    - **Few Ingredients:** overrepresented in the Bayesian Top 100
      (22% vs. 9.33%).
    - **Medium Ingredients:** less represented (49% vs. 59.27%).
    - **Many Ingredients:** slightly less represented
      (29% vs. 31.40%).
    """
)

st.caption(
    "These results describe differences in category representation "
    "and do not establish a causal relationship between the number "
    "of ingredients and recipe ranking."
)
