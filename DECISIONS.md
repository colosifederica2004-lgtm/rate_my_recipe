# Decisions Log

This file explains the main choices made in the project, why they were made, and which alternatives were discarded.

## 1. Raw data kept out of Git

The two CSV files in `data/` are excluded from the repository with `.gitignore`, because they are large and GitHub does not accept files over 100 MB. The README explains how to download them. Committing the full dataset was not an option because of this size limit.

## 2. Rating 0 treated as "no numerical rating"

Interactions with `rating == 0` (60,847 rows, about 5.37% of the 1,132,367 interactions) are excluded from the ranking calculations. The original dataset is left unchanged, and a separate DataFrame (`valid_interactions`) keeps only ratings from 1 to 5.

Two previous analyses of the dataset, Harshi Saha's report *Food.com Interaction and Rating Prediction* and the Recipe-Data-Analytics repository, interpret a 0 as an interaction without a numerical rating. A manual inspection of 30 random zero-rated reviews points in the same direction: 16 are positive, 8 are neutral comments or questions, 6 are critical, and 3 authors explicitly say they did not give a rating.

We considered two alternatives. Treating 0 as a real rating would unfairly lower the average of recipes whose users only left a comment. Replacing 0 with the recipe's average would invent a value that the user never gave.

A consequence of this choice is that 5,047 recipes (about 2.2%) have only zero-rated interactions, so they have no valid rating and cannot be ranked.

This interpretation relies on previous analyses and a small sample, not on official Food.com documentation, and about one fifth of the inspected reviews were critical, so excluding them may slightly raise the averages.

## 3. No sampling of the data

The analysis uses all 1,071,520 valid interactions and all 226,590 recipes with at least one valid rating. The data fit in memory and pandas processes them in seconds. Sampling would also remove most of the recipes with many ratings, which are the most useful to compare the methods: only 787 recipes have 100 or more reviews. A sample could be reconsidered later if the Streamlit app turns out to be slow.

## 4. Two ranking methods compared

We compare a simple average ranking with a Bayesian weighted ranking. The simple average is easy to interpret, but it puts recipes with very few ratings at the top: 110,048 recipes have a perfect average of 5.0 and 59,447 of them have a single rating. The Bayesian average combines each recipe's average with the overall average (4.66), giving more weight to the overall average when a recipe has few ratings. Averages are not rounded before computing the score, to avoid artificial ties.

We also considered keeping only recipes above a minimum number of ratings (a threshold of 10 would leave fewer than 10% of the recipes) and the Wilson lower bound described in the article cited in the assignment. We preferred the Bayesian average because it is simpler to explain and compute. The simple average remains as the baseline for the comparison.

## 5. Bayesian weighting parameter

The parameter `m`, which controls how strongly recipes with few ratings are pulled towards the overall average, is set to 9, the 90th percentile of the number of valid ratings per recipe. This is a data-driven choice, but it remains a project choice and not a universally correct value: a different threshold could change the ranking.