import polars as pl
import os
from lib import statistics, category_counts, visualization, generate_pdf

# Sample inline data as a string, mimicking a CSV structure
inline_data = """
main_category,sub_category,ratings,no_of_ratings,discount_price,actual_price
Electronics,Mobile Phones,4.5,200,500.0,700.0
Electronics,Laptops,4.0,150,1000.0,1200.0
Home Appliances,Refrigerators,3.8,100,300.0,500.0
Home Appliances,Washing Machines,4.2,80,400.0,600.0
"""


def get_inline_dataframe():
    return pl.read_csv(inline_data.encode(), null_values=["null", ""])


def test_load_dataset():
    df = get_inline_dataframe()
    assert isinstance(df, pl.DataFrame), "Data should be loaded as a Polars DataFrame"
    assert "ratings" in df.columns, "ratings column should be present in the dataset"
    assert "no_of_ratings" in df.columns, "no_of_ratings column should be present"


def test_statistics():
    df = get_inline_dataframe()
    stats_df = statistics(df)
    assert "mean_ratings" in stats_df.columns, "Mean ratings should be calculated"
    assert "median_ratings" in stats_df.columns, "Median ratings should be calculated"
    assert len(stats_df) > 0, "Statistics DataFrame should not be empty"


def test_category_counts():
    df = get_inline_dataframe()
    main_category_counts, sub_category_counts = category_counts(df)
    assert len(main_category_counts) == 2, "There should be two main categories"
    assert len(sub_category_counts) == 4, "There should be four subcategories"


def test_visualization():
    df = get_inline_dataframe()
    result = visualization(df)

    # Ensure the images directory exists
    assert os.path.exists("images"), "Images folder should be created"

    # Ensure the saved images exist
    assert os.path.exists(
        "images/main_category_ratings_count_bar_chart.png"
    ), "Bar chart should be saved"
    assert os.path.exists(
        "images/main_category_mean_ratings_bar_chart.png"
    ), "Mean ratings chart should be saved"
    first_category = df["main_category"][0]
    assert os.path.exists(
        f"images/{first_category}_ratings_histogram.png"
    ), f"Histogram for {first_category} should be saved"

    # Ensure the function returns the correct success message
    assert (
        result == "Visualizations saved."
    ), "Visualization should return 'Visualizations saved.' message"


def test_generate_pdf():
    df = get_inline_dataframe()
    stats_df = statistics(df)
    main_category_counts, sub_category_counts = category_counts(df)

    # Create the 'test_outputs' directory if it doesn't exist
    test_output_dir = "test_outputs"
    if not os.path.exists(test_output_dir):
        os.makedirs(test_output_dir)

    # Define the path for the test PDF
    test_pdf_path = os.path.join(test_output_dir, "Amazon_Sales_Report_test.pdf")

    # Generate the PDF
    generate_pdf(
        main_category_counts, sub_category_counts, stats_df, pdf_path=test_pdf_path
    )

    # Check if the PDF was generated
    assert os.path.exists(test_pdf_path), "Test PDF should be generated"
