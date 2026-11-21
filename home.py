"""Home page: project overview, key ideas and dataset summary."""

import streamlit as st

from recipe_project.analysis import load_recipes_with_stats

# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------


@st.cache_data
def load_project_summary():
    """Count the recipes, the valid ratings and the rated recipes."""

    recipes = load_recipes_with_stats(recipe_columns=["id"], how="left")

    total_recipes = len(recipes)
    valid_ratings = int(recipes["rating_count"].sum())
    rated_recipes = int(recipes["rating_count"].notna().sum())

    return total_recipes, valid_ratings, rated_recipes


total_recipes, valid_ratings, rated_recipes = load_project_summary()

# --------------------------------------------------
# CUSTOM STYLE
# --------------------------------------------------

st.markdown(
    """
    <style>
    .hero {
        padding: 20px 0;
        margin-bottom: 10px;
        border-bottom: 1px solid #E8DDF0;
    }

    .hero h1 {
        color: #30243A;
        font-size: 42px;
        margin-bottom: 12px;
    }

    .hero p {
        color: #62556B;
        font-size: 17px;
        margin-bottom: 0;
    }

    .section-intro {
        color: #756B7B;
        font-size: 15px;
    }

    [data-testid="stMetricValue"] {
    font-weight: 700;
    }

    </style>

    <div class="hero">
        <h1>🍽️ Rate My Recipe</h1>
        <p>Discover recipes, explore user ratings and find out what
        makes a recipe stand out.</p>
    </div>
    """,
    unsafe_allow_html=True
)

button_one, button_two, button_three, button_four = st.columns(4)
with button_one:
    st.page_link("pages/1_Explore.py", label="Explore recipes", icon="🔎")
with button_two:
    st.page_link("pages/2_Rankings.py", label="See the rankings", icon="🏆")
with button_three:
    st.page_link("pages/3_Analysis.py", label="Analysis", icon="📊")
with button_four:
    st.page_link("pages/4_Recipe_characteristics.py",
                 label="Characteristics", icon="🥕")


st.subheader("The idea in three steps")

problem_col, solution_col, proof_col = st.columns(3)

with problem_col:
    with st.container(border=True):
        st.markdown("### 1️⃣ The problem")
        st.markdown(
            "**59,447** recipes have a perfect 5.0, but with only "
            "**one** rating. A simple average puts them at the top."
        )

with solution_col:
    with st.container(border=True):
        st.markdown("### 2️⃣ The solution")
        st.markdown(
            "A **Bayesian average** pulls recipes with few ratings "
            "towards the overall mean, so the number of ratings counts."
        )

with proof_col:
    with st.container(border=True):
        st.markdown("### 3️⃣ The proof")
        st.markdown(
            "On ratings the method had never seen, the Bayesian top 100 "
            "scores **4.916**, against **4.683** for the simple average."
        )


# --------------------------------------------------
# DATASET OVERVIEW
# --------------------------------------------------

st.subheader("The Dataset at a Glance")

st.markdown(
    '<p class="section-intro">'
    'A collection of recipes and user ratings from Food.com.</p>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Recipes", f"{total_recipes:,}")

with col2:
    st.metric("Valid Ratings", f"{valid_ratings:,}")

with col3:
    st.metric("Recipes with Ratings", f"{rated_recipes:,}")

st.divider()

st.caption(
    "Rate My Recipe | A data-driven exploration of recipe ratings "
    "and rankings. Data: [Food.com Recipes and Interactions on Kaggle]"
    "(https://www.kaggle.com/datasets/shuyangli94/"
    "food-com-recipes-and-user-interactions)."
)
