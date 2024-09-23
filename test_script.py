import os
from script import main


def test_main():
    """Test the main function to ensure everything works end-to-end."""
    main()
    assert os.path.exists("images"), "Images folder should be created"
    assert os.path.exists("Amazon_Sales_Report.pdf"), "PDF should be generated"
    assert os.path.exists(
        "images/main_category_ratings_count_bar_chart.png"
    ), "Bar chart should be saved"
    assert os.path.exists(
        "images/main_category_mean_ratings_bar_chart.png"
    ), "Mean ratings chart should be saved"
