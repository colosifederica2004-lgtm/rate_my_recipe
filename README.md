# 🍽️ Rate My Recipe

Rate My Recipe is a data analysis project based on the Food.com Recipes and Interactions dataset. It explores how users rate recipes and develops a ranking strategy that considers both average ratings and the number of ratings received.

## What the app does

The application has five pages:

| Page | What you can do |
|------|-----------------|
| **Home** (`app.py`) | Overview of the project and key information about the dataset. |
| **Explore** (`pages/1_Explore.py`) | Search recipes by name and filter them by preparation time, number of ingredients and minimum average rating. |
| **Rankings** (`pages/2_Rankings.py`) | Explore and compare recipes ranked using Simple Average Ranking and Bayesian Weighted Ranking. |
| **Analysis** (`pages/3_Analysis.py`) | Compare the two ranking methods through interactive visualizations and statistical insights. |
| **Recipe Characteristics** (`pages/4_Recipe_Characteristics.py`) | Explore how preparation time and number of ingredients are represented in the Bayesian Weighted Ranking. |

### How the ranking works

The project compares two ranking methods:

- **Simple Average Ranking:** recipes are ranked according to their average user rating.
- **Bayesian Weighted Ranking:** recipes are ranked using a weighted average that considers both their average rating and the number of ratings received.

The Bayesian score is calculated as:

\[
Score = \frac{v}{v+m}R + \frac{m}{v+m}C
\]

Where:
- \(R\) is the recipe's average rating.
- \(v\) is the number of ratings received by the recipe.
- \(C\) is the global average rating.
- \(m\) is a minimum rating threshold, set using the 90th percentile of the number of ratings.

This approach gives more weight to the global average for recipes with fewer ratings, reducing the influence of recipes with very few reviews.

## Data sources

The project uses the **Food.com Recipes and Interactions dataset**, available on Kaggle:

- [Food.com Recipes and User Interactions](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions)

The dataset contains two files:
- `RAW_recipes.csv`: recipe information, including names, preparation time, ingredients and tags.
- `RAW_interactions.csv`: user interactions, including recipe IDs and ratings.

The original dataset files are not included in the repository because of their size. They must be downloaded separately and placed in the `data/` directory.

## Libraries

| Library | Used for |
|---------|----------|
| `pandas` | Loading, cleaning and analysing datasets. |
| `numpy` | Numerical operations and data processing. |
| `matplotlib` | Data visualization in the notebooks. |
| `seaborn` | Statistical visualizations in the notebooks. |
| `plotly` | Interactive charts in the application. |
| `streamlit` | Building the interactive web application. |

Exact dependencies are listed in `requirements.txt`.

## Setup

1. Clone or download the repository and enter the project folder.

2. Create a virtual environment and install the dependencies:

   ```bash
   python -m venv .venv
   ```

   Activate it:

   ```bash
   # Windows
   .venv\Scripts\activate

   # macOS / Linux
   source .venv/bin/activate
   ```

   Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

3. Download the Food.com dataset from Kaggle and place the following files inside the `data/` directory:

   ```text
   data/
   ├── RAW_recipes.csv
   └── RAW_interactions.csv
   ```

## Run

Start the Streamlit application from the project root:

```bash
streamlit run app.py
```

The application will be available at:

<http://localhost:8501>

Use the sidebar to navigate between the different pages.

### The notebooks

The project includes two Jupyter notebooks documenting the data analysis process:

- `notebooks/01_dataset_exploration.ipynb`: dataset exploration, data cleaning, ranking development and evaluation.
- `notebooks/02_recipe_characteristics.ipynb`: analysis of recipe characteristics, focusing on preparation time and number of ingredients.

Start Jupyter from the project root:

```bash
jupyter lab
```

Open the notebooks to explore the analysis step by step.

## Project structure

```text
rate_my_recipe/
├── app.py
├── pages/
│   ├── 1_Explore.py
│   ├── 2_Rankings.py
│   ├── 3_Analysis.py
│   └── 4_Recipe_Characteristics.py
├── recipe_project/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── cleaning.py
│   ├── analysis.py
│   ├── plots.py
│   └── ranking.py
├── notebooks/
│   ├── 01_dataset_exploration.ipynb
│   └── 02_recipe_characteristics.ipynb
├── data/
├── .gitignore
├── requirements.txt
└── README.md
```