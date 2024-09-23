# Seijung Kim (sk591)
# This script has functions for data cleaning,
# generating descriptive stats, data viz, and a pdf

import os
import polars as pl
import matplotlib.pyplot as plt
from fpdf import FPDF


def load_dataset(data_path):
    """Read the CSV file using polars"""
    df = pl.read_csv(
        data_path,
        null_values=["null", ""],  # Treat empty strings and "null" as missing
        infer_schema_length=1000,  # Adjust this if the schema isn't inferred correctly
    )

    # Clean and convert 'ratings' by removing non-numeric values
    df = df.with_columns(
        pl.col("ratings")
        .str.replace_all(
            "[^0-9.]", ""
        )  # Keep only numeric characters and decimal points
        .cast(pl.Float64, strict=False)
    )

    # Clean and convert 'no_of_ratings' by removing non-numeric values
    df = df.with_columns(
        pl.col("no_of_ratings")
        .str.replace_all("[^0-9]", "")  # Keep only numeric characters
        .cast(
            pl.Int64, strict=False
        )  # Cast to integer, allowing conversion failures (set to null)
    )

    # Clean and convert 'discount_price' and 'actual_price'
    df = df.with_columns(
        [
            pl.col("discount_price")
            .str.replace_all("[₹,]", "")  # Remove ₹ and commas
            .cast(pl.Float64),  # Convert to float
            pl.col("actual_price")
            .str.replace_all("[₹,]", "")  # Remove ₹ and commas
            .cast(pl.Float64),  # Convert to float
        ]
    )

    # Drop rows with missing (null) values
    df = df.drop_nulls()

    return df


def statistics(df):
    """Function to calculate statistics for each main_category"""

    # Group by main_category and calculate descriptive statistics using Polars
    stats = (
        df.group_by("main_category")
        .agg(
            [
                # ratings
                pl.col("ratings").mean().alias("mean_ratings"),
                pl.col("ratings").median().alias("median_ratings"),
                pl.col("ratings").std().alias("std_ratings"),
                # number of ratings
                pl.col("no_of_ratings").mean().alias("mean_no_of_ratings"),
            ]
        )
        .sort("main_category")
    )

    # Convert the result to a Pandas DataFrame to save or further process
    stats_pandas = stats.to_pandas()

    return stats_pandas


def category_counts(df):
    """Function to track counts of main_category and sub_category using Polars"""

    # Track counts for main_category using Polars and explicitly name the count column
    main_category_counts = (
        df.group_by("main_category")
        .agg(pl.col("main_category").count().alias("counts"))
        .sort("main_category")
    )
    df_main_category_counts = main_category_counts.to_pandas()

    # Track counts for sub_category using Polars and explicitly name the count column
    sub_category_counts = (
        df.group_by("sub_category")
        .agg(pl.col("sub_category").count().alias("counts"))
        .sort("sub_category")
    )
    df_sub_category_counts = sub_category_counts.to_pandas()

    return (
        df_main_category_counts,
        df_sub_category_counts,
    )  # Return as Pandas DataFrames


def visualization(df_input):
    """Function to draw bar graphs and histograms for each main_category"""

    # Convert Polars DataFrame to Pandas if it is still a Polars DataFrame
    if isinstance(df_input, pl.DataFrame):
        df_input = df_input.to_pandas()

    # Histogram of ratings for one of the main categories
    first_category = df_input["main_category"].unique()[0]  # Get the first category
    subset = df_input[df_input["main_category"] == first_category]
    plt.figure(figsize=(10, 6))
    subset["ratings"].hist(bins=20, color="#93C572")
    plt.title(f"Ratings Distribution for {first_category}")
    plt.xlabel("Ratings")
    plt.ylabel("Frequency")
    plt.tight_layout()  # Prevents labels from being cut off
    plt.savefig(f"images/{first_category}_ratings_histogram.png")
    plt.close()

    # Bar graph: counts of ratings for each main category
    plt.figure(figsize=(10, 6))
    ratings_counts = df_input.groupby("main_category")["ratings"].count()
    ratings_counts.plot(kind="bar", color="#ADD8E6")
    plt.title("Counts of Ratings for Each Main Category")
    plt.xlabel("Main Category")
    plt.ylabel("Count of Ratings")
    plt.tight_layout()  # Prevents labels from being cut off
    plt.savefig("images/main_category_ratings_count_bar_chart.png")
    plt.close()

    # Bar graph: mean ratings for each main category
    plt.figure(figsize=(10, 6))
    mean_ratings = df_input.groupby("main_category")["ratings"].mean()
    mean_ratings.plot(kind="bar", color="#ADD8E6")
    plt.title("Mean Ratings for Each Main Category")
    plt.xlabel("Main Category")
    plt.ylabel("Mean Ratings")
    plt.tight_layout()  # Prevents labels from being cut off
    plt.savefig("images/main_category_mean_ratings_bar_chart.png")
    plt.close()

    return "Visualizations saved."


def generate_pdf(
    main_category_counts,
    sub_category_counts,
    stats_df,
    pdf_path="Amazon_Sales_Report.pdf",
):
    """Generate Amazon sales dataset report and save it to PDF."""
    pdf = FPDF()

    # Add a page for category counts
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Amazon Sales Dataset Report", ln=True, align="C")

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="Counts of Main Categories", ln=True, align="L")

    # Add main category counts as a table
    pdf.set_font("Arial", "", 10)
    for index, row in main_category_counts.iterrows():
        pdf.cell(100, 10, txt=f'{row["main_category"]}', border=1)
        pdf.cell(100, 10, txt=f'{row["counts"]}', border=1, ln=True)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="Counts of Sub Categories", ln=True, align="L")
    pdf.set_font("Arial", "", 10)
    for index, row in sub_category_counts.iterrows():
        pdf.cell(100, 10, txt=f'{row["sub_category"]}', border=1)
        pdf.cell(100, 10, txt=f'{row["counts"]}', border=1, ln=True)

    # Add a page for overall statistics
    pdf.add_page()
    pdf.set_font("Arial", "B", 10)
    pdf.cell(
        200,
        10,
        txt="Descriptive Statistics for Ratings and Number of Ratings",
        ln=True,
        align="L",
    )

    # Convert statistics DataFrame into a table and display it in the PDF
    pdf.set_font("Arial", "", 10)
    pdf.set_xy(10, 30)
    pdf.multi_cell(
        200, 10, stats_df.to_string(index=False)
    )  # Add statistics as a table
    pdf.ln(10)

    # Add the bar chart images
    if os.path.exists("images/main_category_ratings_count_bar_chart.png"):
        pdf.add_page()
        pdf.cell(200, 10, txt="Counts of Ratings for Each Main Category", ln=True)
        pdf.image("images/main_category_ratings_count_bar_chart.png", x=10, y=30, w=190)

    if os.path.exists("images/main_category_mean_ratings_bar_chart.png"):
        pdf.add_page()
        pdf.cell(200, 10, txt="Mean Ratings for Each Main Category", ln=True)
        pdf.image("images/main_category_mean_ratings_bar_chart.png", x=10, y=30, w=190)

    # Add the histograms for ratings distribution
    categories = stats_df["main_category"].unique()
    for category in categories:
        histogram_path = f"images/{category}_ratings_histogram.png"
        if os.path.exists(histogram_path):
            pdf.add_page()
            pdf.cell(200, 10, txt=f"Ratings Distribution for {category}", ln=True)
            pdf.image(histogram_path, x=10, y=30, w=190)

    # Output the PDF to a file
    pdf.output(pdf_path)
    print(f"PDF report generated: {pdf_path}")


if __name__ == "__main__":

    data_path = "Amazon-Products-100k.csv"

    # Load the dataset using polars
    df = load_dataset(data_path)

    # Perform statistics for each main category
    stats_df = statistics(df)
    # print("Statistics calculated:")
    # print(stats_df)

    main_category_counts, sub_category_counts = category_counts(df)
    # print("Main Category Counts:")
    # print(main_category_counts)
    # print("Sub Category Counts:")
    # print(sub_category_counts)

    # Generate visualizations
    print(visualization(df))

    # Generate the PDF report
    generate_pdf(main_category_counts, sub_category_counts, stats_df)
