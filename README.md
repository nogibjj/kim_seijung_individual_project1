Check CI/CD Status:


# Mini-project #2
#### repo title: kim_seijung_individual_project1
#### Author: Seijung Kim (sk591)

## Overview
This project is for creating a Python that utilizes the Pandas Library to load a dataset and generate different summary statistics for Exploratory Data Analysis. The generated data visualization and summary report should serve as useful tools to understand the dataset and its variables. You can load this repository to a codespace and make the devcontainer execute the Makefile that will run the following: install, format, lint, test.


# Requirements

Project #1: Continuous Integration using Gitlab Actions of Python Data Science Project

The project structure must include the following files:
* Jupyter Notebook with: 
    * Cells that perform descriptive statistics using Polars or Panda.
    * Tested by using nbval plugin for pytest

* Makefile with the following:
    * Run all tests (must test notebook and script and lib)
    * Formats code with Python blackLinks to an external site.
    * Lints code with RuffLinks to an external site.
    * Installs code via:  pip install -r requirements.txt

* test_script.py to test script
* test_lib.py to test library
* Pinned requirements.txt
* Gitlab Actions performs all four Makefile commands with badges for each one in the README.md


# About the Dataset
![Alt text](path/to/Amazon-Logo.webp)

The `Amazon-Products-100k.csv` file used in this project is from the Amazon Products Sales Dataset 2023, obtained via Kaggle (). This is a product sales dataset scraped from the Amazon website from the year 2023, including a total of 142 item categories such as Fine Art, Dog Supplies, etc. The csv file was truncated to contain the first 100k rows of data from the original full products csv file due to the large size and memory limits for GitHub storage. The csv file consists of 10 columns with a row number and the following 9 variables.

| **Variable**      | **Description**                                                          |
|-------------------|--------------------------------------------------------------------------|
| `name`            | The name of the product                                                  |
| `main_category`   | The main category the product belongs to                                 |
| `sub_category`    | The sub-category the product belongs to                                  |
| `image`           | The image representing the product                                       |
| `link`            | The Amazon website reference link of the product                         |
| `ratings`         | The ratings given by Amazon customers for the product                    |
| `no of ratings`   | The number of ratings given to the product on Amazon                     |
| `discount_price`  | The discount price of the product                                        |
| `actual_price`    | The actual MRP (Maximum Retail Price) of the product                     |


