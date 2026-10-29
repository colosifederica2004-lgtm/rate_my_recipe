# Decisions Log

This file records the main choices made in the project, with the reason and the alternatives discarded.

## 1. Project topic: Rate My Recipe

**Choice:** Rank recipes from the Food.com Recipes and Interactions dataset by user ratings.

**Reason:** The dataset has a clear problem to solve: recipes have very different numbers of reviews (median 2, maximum 1,613), so a simple average rating is misleading.

**Alternatives discarded:** "Powering the Planet" (energy and CO2 data), because merging several datasets made the project more complex.

## 2. Raw data kept out of Git

**Choice:** The two CSV files in `data/` are excluded with `.gitignore`; the README explains how to download them.

**Reason:** The files are large and GitHub does not accept files over 100 MB.

**Alternatives discarded:** Committing the full data (not possible because of the size).

## 3. Rating 0 treated as "no rating given"

## 3. Rating 0 treated as "no numerical rating"

**Choice:** Interactions with `rating == 0` (60,847 rows, approximately 5.37% of 1,132,367 interactions) will be excluded from ranking calculations. The original dataset will remain unchanged, and a separate filtered DataFrame will be used.

**Reason:** Two previous analyses of the dataset interpret a rating of 0 as an interaction without a numerical rating: [Harshi Saha's project report, *Food.com Interaction and Rating Prediction*](https://harshi-saha.github.io/files/food-com-project.pdf) and the [Recipe-Data-Analytics repository](https://github.com/danielpwarren/Recipe-Data-Analytics). A manual inspection of 30 zero-rated reviews also showed that review text can express different opinions, so the text alone cannot reliably determine a numerical rating.

**Alternatives discarded:**
- Treat 0 as a valid numerical rating: this could unfairly lower the average rating of recipes with zero-rated interactions.
- Replace 0 with the recipe's average rating: this would assign a numerical value that the user did not provide.

**Limitation:** This interpretation is based on previous analyses of the dataset, not official Food.com documentation. The manual inspection involved only a small sample and cannot establish the meaning of every zero-rated interaction. Excluding these interactions may affect recipe rankings. Where feasible, the ranking results will be compared under alternative treatments of zero ratings to assess the impact of this decision.