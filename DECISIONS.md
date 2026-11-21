# Decisions Log

This file explains the main decisions made in the project, the reason behind them, and the alternatives considered.

## 1. Raw data kept out of Git

The two CSV files in `data/` are excluded from the repository through `.gitignore` because of their large size. The README explains how to download them separately.

Keeping the full dataset in the repository was not considered practical because GitHub limits individual files to 100 MB.

## 2. Rating 0 treated as "no numerical rating"

Interactions with `rating == 0` (60,847 rows, about 5.37% of the 1,132,367 interactions) are excluded from the ranking calculations.

The original dataset is left unchanged, and a separate DataFrame (`valid_interactions`) keeps only ratings from 1 to 5.

Two previous analyses of the dataset, Harshi Saha's report *Food.com Interaction and Rating Prediction* and the Recipe-Data-Analytics repository, interpret a 0 as an interaction without a numerical rating.

We considered two alternatives:
- Treating 0 as a real rating would unfairly lower the average of recipes whose users only left a comment.
- Replacing 0 with the recipe's average would introduce a value that the user never provided.

As a consequence, 5,047 recipes (approximately 2.2%) have only zero-rated interactions and therefore cannot be ranked.

This interpretation relies on previous analyses, not on official Food.com documentation, so the meaning of a rating of 0 cannot be considered definitively established. If some zero-rated interactions were actually negative evaluations, excluding them may slightly increase the average ratings.

## 3. No sampling of the data

The analysis uses all 1,071,520 valid interactions and all 226,590 recipes with at least one valid rating.

The dataset fits in memory and can be processed with pandas in a reasonable amount of time. Sampling would also reduce the number of recipes with many ratings, which are particularly useful when comparing ranking methods. 

Only 787 recipes have 100 or more reviews. The Streamlit app loads only the columns it needs and caches the prepared data, so sampling was not necessary.

## 4. Two Ranking Methods Compared

The project compares Simple Average Ranking with Bayesian Weighted Ranking.

The simple average is easy to interpret, but it can place recipes with very few ratings at the top. In particular, 110,048 recipes have a perfect average rating of 5.0, and 59,447 of these have only one rating.

The Bayesian Weighted Ranking combines each recipe's average rating with the global average (4.66), giving more weight to the global average when a recipe has fewer ratings.

Average ratings are not rounded before calculating the Bayesian score, in order to avoid introducing artificial ties. Ties are broken in a reproducible way: recipes are sorted by id and the sorting is stable.

The Simple Average Ranking is retained as a baseline for comparison with the proposed Bayesian approach.

## 5. Bayesian weighting parameter

The parameter `m`, which controls how strongly recipes with few ratings are pulled towards the overall average, is set to 9. This value corresponds to the 90th percentile of the number of valid ratings per recipe.

This is a data-driven choice, but it is not a universally optimal value. Choosing a different threshold could chnage the resulting ranking. 

## 6. Validation of the rankings

To check which ranking identifies recipes that users actually like, the valid ratings are randomly split into two halves (train and test, seed 42, so the split is reproducible).

Both rankings are built using only the train half. For this reason, C and m are recalculated on the train half (C = 4.66, m = 6, with the same 90th percentile criterion), so that no information from the test half is used to build the rankings. The test half is used only to measure the result.

Only recipes with at least one rating in the test half can be evaluated. For the top 100 and top 1,000 recipes of each ranking, we compute the mean test rating, weighting each recipe by its number of test ratings. The baseline is the mean test rating of all the evaluated recipes (4.685).

Results: Bayesian 4.916 against 4.683 for the simple average (top 100), and 4.864 against 4.630 (top 1,000).

Limitations: the evaluation uses a single random split; the split is made on interactions, not on users, so the same user can appear in both halves; only recipes with ratings in both halves are evaluated. We did not run extra statistical tests.

## 7. Preparation time: invalid values and categories

The preparation time contains 1,094 recipes with zero minutes and 2,240 recipes above 1,000 minutes (the maximum is 2,147,483,647). These values would distort the analysis, so recipes with zero minutes or more than 1,000 minutes are excluded from the preparation time analysis only. The threshold is an operational choice, not proof that every excluded value is wrong.

Recipes are grouped into four categories: Quick (up to 30 minutes), Medium (31-60), Long (61-90) and Very Long (over 90).

## 8. Number of ingredients: categories

Recipes are grouped into three categories: Few Ingredients (1-4), Medium Ingredients (5-10) and Many Ingredients (more than 10).

For both preparation time and ingredients, we compare the share of each category among the top 100 recipes of the Bayesian ranking with its share among all the ranked recipes. This describes an association and does not establish a causal relationship.

## 9. Shared code between notebooks and app

The logic (data loading, cleaning, categories, rankings and validation) is written once in the `recipe_project` package. Notebooks and app only call these functions, so they show the same numbers and nothing is duplicated.