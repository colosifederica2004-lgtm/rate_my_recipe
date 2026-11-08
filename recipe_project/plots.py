
"""Functions to create visualizations for the Rate My Recipe project."""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def apply_style(ax, title, xlabel, ylabel):
    """
    Apply a consistent style to a chart.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The chart axes.
    title : str
        Chart title.
    xlabel : str
        Label for the x-axis.
    ylabel : str
        Label for the y-axis.
    """
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", alpha=0.3)


def rating_distribution(interactions):
    """
    Create a bar chart showing the distribution of recipe ratings.

    Parameters
    ----------
    interactions : pandas.DataFrame
        DataFrame containing user ratings.

    Returns
    -------
    matplotlib.figure.Figure
        The rating distribution chart.
    """
    rating_counts = interactions["rating"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        x=rating_counts.index,
        y=rating_counts.values,
        ax=ax
    )

    apply_style(
        ax,
        "Distribution of Recipe Ratings",
        "Rating",
        "Number of Interactions"
    )

    ax.set_xticks(range(6))
    fig.tight_layout()

    return fig


def review_count_distribution(reviews_per_recipe):
    """
    Create a histogram showing the distribution of reviews per recipe.

    Parameters
    ----------
    reviews_per_recipe : pandas.Series
        Number of reviews for each recipe.

    Returns
    -------
    matplotlib.figure.Figure
        The review count distribution chart.
    """
    fig, ax = plt.subplots(figsize=(9, 5))

    sns.histplot(
        x=reviews_per_recipe,
        bins=50,
        ax=ax
    )

    apply_style(
        ax,
        "Distribution of Reviews per Recipe",
        "Number of Reviews",
        "Number of Recipes"
    )

    ax.set_xscale("log")
    fig.tight_layout()

    return fig


def ranking_comparison(simple_ranking, weighted_ranking, top_n=1000):
    """
    Compare the number of ratings received by recipes
    in the top results of the two ranking strategies.

    Parameters
    ----------
    simple_ranking : pandas.DataFrame
        Ranking based on the simple average.
    weighted_ranking : pandas.DataFrame
        Ranking based on the Bayesian weighted score.
    top_n : int
        Number of top recipes to compare.

    Returns
    -------
    matplotlib.figure.Figure
        The ranking comparison boxplot.
    """
    simple_counts = simple_ranking.head(top_n)["rating_count"]
    weighted_counts = weighted_ranking.head(top_n)["rating_count"]

    comparison = pd.DataFrame({
        "Ranking": (
            ["Simple Average"] * len(simple_counts)
            + ["Bayesian Weighted"] * len(weighted_counts)
        ),
        "Number of Reviews": pd.concat(
            [simple_counts, weighted_counts]
        ).values
    })

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.boxplot(
        data=comparison,
        x="Ranking",
        y="Number of Reviews",
        ax=ax
    )

    apply_style(
        ax,
        f"Review Count Comparison (Top {top_n} Recipes)",
        "Ranking Strategy",
        "Number of Reviews"
    )

    ax.set_yscale("log")
    fig.tight_layout()

    return fig