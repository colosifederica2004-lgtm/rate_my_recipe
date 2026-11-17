import streamlit as st
import plotly.express as px

from recipe_project.data_loader import load_recipes, load_interactions
from recipe_project.cleaning import filter_valid_interactions
from recipe_project.analysis import calculate_recipe_stats
from recipe_project.ranking import (
    simple_average_ranking,
    bayesian_weighted_ranking
)

# Page title
st.title("📊 Recipe Analysis")

st.write(
    """
    Explore the differences between Simple Average Ranking
    and Bayesian Weighted Ranking through interactive
    visualizations and statistical insights.
    """
)

@st.cache_data
def load_analysis_data():
    """Load and prepare data for ranking analysis."""

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

# Load data
recipes_with_stats = load_analysis_data()

# Calculate rankings
simple_ranking = simple_average_ranking(recipes_with_stats)
bayesian_ranking = bayesian_weighted_ranking(recipes_with_stats)

st.divider()

st.subheader("Comparing the Two Ranking Methods")

st.write(
    "Explore how recipe positions change between "
    "Simple Average Ranking and Bayesian Weighted Ranking."
)

top_n = st.selectbox(
    "Number of top recipes to compare",
    [100, 500, 1000, 2000, 5000, 10000],
    index=1
)

# Select the top N recipes from each ranking
simple_top = simple_ranking.head(top_n).copy()
bayesian_top = bayesian_ranking.head(top_n).copy()

# Add ranking positions
simple_top["simple_position"] = range(1, len(simple_top) + 1)
bayesian_top["bayesian_position"] = range(1, len(bayesian_top) + 1)

# Find recipes appearing in both rankings
common_recipes = simple_top.merge(
    bayesian_top,
    on="recipe_id",
    suffixes=("_simple", "_bayesian")
)


# Calculate comparison metrics
common_count = len(common_recipes)

common_percentage = (common_count / top_n) * 100

# Display metrics
st.subheader("Ranking Comparison Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Recipes Compared",
    f"{top_n:,}"
)

col2.metric(
    "Common Recipes",
    f"{common_count:,}"
)

col3.metric(
    "Common Recipes (%)",
    f"{common_percentage:.2f}%"
)

# Display ranking positions
st.subheader("Ranking Position Comparison")

if common_recipes.empty:

    st.info(
        "No recipes appear in both selected rankings. "
        "Try increasing the number of recipes to compare."
    )

else:

    comparison_table = common_recipes[
        [
            "name_simple",
            "simple_position",
            "bayesian_position",
            "rating_count_simple",
            "average_rating_simple",
            "bayesian_score"
        ]
    ].copy()

    # Rename columns for a clearer presentation
    comparison_table = comparison_table.rename(
        columns={
            "name_simple": "Recipe",
            "simple_position": "Simple Pos.",
            "bayesian_position": "Bayesian Pos",
            "rating_count_simple": "Ratings",
            "average_rating_simple": "Avg. Rating",
            "bayesian_score": "Bayesian Score"
        }
    )

    # Display the comparison table
    st.dataframe(
        comparison_table,
        use_container_width=True,
        hide_index=True,
        column_config={
        "Recipe": st.column_config.TextColumn(
            width="large"
        ),
        "Simple Average Position": st.column_config.NumberColumn(
            format="%d",
            width="small"
        ),
        "Bayesian Weighted Position": st.column_config.NumberColumn(
            format="%d",
            width="small"
        ),
        "Number of Ratings": st.column_config.NumberColumn(
            format="%d",
            width="small"
        ),
        "Average Rating": st.column_config.NumberColumn(
            format="%.2f",
            width="small"
        ),
        "Bayesian Score": st.column_config.NumberColumn(
            format="%.3f",
            width="small"
        )
    }
    )

    # Calculate the change in ranking position
    common_recipes["position_change"] = (
        common_recipes["simple_position"]
        - common_recipes["bayesian_position"]
    )

    fig_modern = px.scatter(
        common_recipes,
        x="simple_position",
        y="bayesian_position",
        color="position_change",
        color_continuous_scale=[
            [0.0, "#E75480"],
            [0.5, "#D8B4E2"],
            [1.0, "#7B2CBF"]
        ],
        hover_name="name_simple",
        hover_data={
            "simple_position": True,
            "bayesian_position": True,
            "rating_count_simple": True,
            "average_rating_simple": ":.2f",
            "bayesian_score": ":.3f",
            "position_change": True
        },
        labels={
            "simple_position": "Simple Average Position",
            "bayesian_position": "Bayesian Weighted Position",
            "position_change": "Position improvement",
            "rating_count_simple": "Number of Ratings",
            "average_rating_simple": "Average Rating",
            "bayesian_score": "Bayesian Score"
        }
    )

    fig_modern.add_shape(
        type="line",
        x0=0, y0=0,
        x1=top_n, y1=top_n,
        line=dict(color="#999999", dash="dash", width=1.5)
    )

    fig_modern.update_traces(
        marker=dict(size=11, opacity=0.85,line=dict(width=1.5, color="white"))
    )

    fig_modern.update_layout(
        title="How Recipes Move Between Rankings",
        template="plotly_white",
        height=520,
        coloraxis_colorbar_title="Position<br>improvement",
        margin=dict(l=30, r=30, t=70, b=30),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Arial",
            color="#000000"
        ),
        title_font=dict(
            size=20,
            color="#000000"
        )   
    )

    fig_modern.update_xaxes(range=[0, top_n])
    fig_modern.update_yaxes(
        range=[0, top_n],
        scaleanchor="x",
        scaleratio=1
    )

    st.plotly_chart(fig_modern, width="stretch")

    st.markdown("### 💡 How to interpret the results")

st.write(
    """
    Recipes below the diagonal line improve their position in the
    Bayesian ranking, while recipes above the line move down.

    This highlights how considering the number of ratings, together
    with the average rating, can change the position of recipes
    in the final ranking.
    """
)

