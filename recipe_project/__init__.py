"""
recipe_project - a package to analyse recipe ratings and build recipe rankings.

The package is organised in modules, each one with a single responsibility:

- ``data_loader`` : load the Food.com CSV datasets
- ``cleaning``    : clean and prepare the data for analysis
- ``analysis``    : perform statistical analysis and aggregate recipe data
- ``ranking``     : calculate and compare Simple Average and Bayesian rankings
- ``plots``       : create charts using matplotlib and seaborn
"""

__version__ = "0.1.0"