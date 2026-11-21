<h1 align="center">🍽️ Rate My Recipe</h1>

<p align="center">
  <em>Which recipes do users really like? A fair ranking that looks at both the average rating and the number of ratings.</em>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white">
  <img alt="pandas" src="https://img.shields.io/badge/pandas-150458?logo=pandas&logoColor=white">
  <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white">
  <img alt="Jupyter" src="https://img.shields.io/badge/Jupyter-F37626?logo=jupyter&logoColor=white">
</p>

Rate My Recipe is a data analysis project based on the Food.com Recipes and Interactions dataset. It explores how users rate recipes and develops a ranking strategy that considers both average ratings and the number of ratings received.

## 🖥️ What the app does

The application has five pages:

| Page | What you can do |
|------|-----------------|
| **Home** (`home.py`) | Overview of the project and key information about the dataset. |
| **Explore** (`pages/1_Explore.py`) | Search recipes by name and filter them by preparation time, number of ingredients and minimum average rating. |
| **Rankings** (`pages/2_Rankings.py`) | Explore and compare recipes ranked using Simple Average Ranking and Bayesian Weighted Ranking. |
| **Analysis** (`pages/3_Analysis.py`) | Compare the two ranking methods through interactive visualizations and statistical insights. |
| **Recipe Characteristics** (`pages/4_Recipe_characteristics.py`) | Examine preparation time and number of ingredients in relation to recipe ratings and their representation in the Bayesian Weighted Ranking. |

### 🧮 How the ranking works

The project compares two ranking methods:

- **Simple Average Ranking:** recipes are ranked according to their average user rating.
- **Bayesian Weighted Ranking:** recipes are ranked using a weighted average that considers both their average rating and the number of ratings received.

The Bayesian score is calculated as:

$$
Score = \frac{v}{v+m}R + \frac{m}{v+m}C
$$

Where:
- $R$ is the recipe's average rating.
- $v$ is the number of valid ratings received by the recipe.
- $C$ is the global average rating (4.66).
- $m$ is a minimum rating threshold, set to the 90th percentile of the number of ratings per recipe (m = 9).

This approach gives more weight to the global average for recipes with fewer ratings, reducing the influence of recipes with very few reviews.

> [!NOTE]
> Ratings equal to 0 are treated as "no numerical rating" and excluded from the calculations. The reasons for this and the other main choices are explained in [DECISIONS.md](DECISIONS.md).

## 📊 Main results

- Of the 1,132,367 interactions, 1,071,520 have a valid rating (1 to 5) and 226,590 recipes can be ranked.
- With the simple average, 110,048 recipes have a perfect score of 5.0 and 59,447 of them have a single rating. The Bayesian average avoids this: its top recipes have far more ratings.
- **Validation.** The ratings were randomly split into two halves: both rankings were built on the first half and evaluated on the second. The mean test rating of the top recipes is higher for the Bayesian ranking.

  | Top recipes | Simple average | Bayesian average |
  |-------------|----------------|------------------|
  | Top 100 | 4.683 | 4.916 |
  | Top 1,000 | 4.630 | 4.864 |

  The mean test rating of all the evaluated recipes is 4.685. The evaluation uses a single random split of the interactions, so it should be interpreted with caution.
- **Recipe characteristics.** Preparation time is not strongly associated with the position in the Bayesian ranking, while recipes with few ingredients are more represented in the top 100 (22%) than in the full ranking (9.33%). These results are descriptive and do not establish a causal relationship.

## 📚 Data sources

The project uses the **Food.com Recipes and Interactions dataset**, available on Kaggle:

- [Food.com Recipes and User Interactions](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions)

The dataset contains two files:
- `RAW_recipes.csv`: recipe information, including names, preparation time, ingredients and tags.
- `RAW_interactions.csv`: user interactions, including recipe IDs and ratings.

The original dataset files are not included in the repository because of their size. They must be downloaded separately and placed in the `data/` directory.

## 🧰 Libraries

| Library | Used for |
|---------|----------|
| `pandas` | Loading, cleaning and analysing datasets. |
| `numpy` | Numerical operations and data processing. |
| `matplotlib` | Data visualization in the notebooks. |
| `seaborn` | Statistical visualizations in the notebooks. |
| `plotly` | Interactive charts in the application. |
| `streamlit` | Building the interactive web application. |
| `jupyterlab` | Running the notebooks. |

Exact dependencies are listed in `requirements.txt`.

## ⚙️ Setup

The project was developed with Python 3.14.

1. Clone the repository and enter the project folder:

   ```bash
   git clone https://github.com/colosifederica2004-lgtm/rate_my_recipe.git
   cd rate_my_recipe
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate it:

   ```bash
   # Windows
   .venv\Scripts\activate

   # macOS / Linux
   source .venv/bin/activate
   ```

4. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

5. Download the Food.com dataset from Kaggle and place the following files inside the `data/` directory:

   ```text
   data/
   ├── RAW_recipes.csv
   └── RAW_interactions.csv
   ```

## ▶️ Run the application

Start the Streamlit application from the project root:

```bash
streamlit run app.py
```

The application will be available at:

<http://localhost:8501>

Use the sidebar to navigate between the different pages.

### 📓 The notebooks

The project includes two Jupyter notebooks documenting the data analysis process:

- `notebooks/01_dataset_exploration.ipynb`: dataset exploration, data cleaning, ranking development and evaluation.
- `notebooks/02_recipe_characteristics.ipynb`: analysis of recipe characteristics, focusing on preparation time and number of ingredients.

Start Jupyter from the project root:

```bash
jupyter lab
```

Open the notebooks to explore the analysis step by step.

## 🗂️ Project structure

```text
rate_my_recipe/
├── app.py
├── home.py
├── pages/
│   ├── 1_Explore.py
│   ├── 2_Rankings.py
│   ├── 3_Analysis.py
│   └── 4_Recipe_characteristics.py
├── recipe_project/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── cleaning.py
│   ├── analysis.py
│   ├── ranking.py
│   └── plots.py
├── notebooks/
│   ├── 01_dataset_exploration.ipynb
│   └── 02_recipe_characteristics.ipynb
├── data/
│   └── .gitkeep
├── .gitattributes
├── .gitignore
├── DECISIONS.md
├── requirements.txt
└── README.md
```

The `recipe_project` package contains the code shared by the notebooks and the app:

- `data_loader.py`: loads the CSV files and checks their structure.
- `cleaning.py`: keeps valid ratings and assigns preparation time and ingredient categories.
- `analysis.py`: recipe statistics, train-test validation and category comparison.
- `ranking.py`: Simple Average and Bayesian Weighted rankings.
- `plots.py`: charts for the notebooks.