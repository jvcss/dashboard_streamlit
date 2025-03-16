import pandas as pd

# Attempt to import IPython display utilities.
try:
    from IPython.display import display, HTML
    _HAS_IPYTHON = True
except ImportError:
    _HAS_IPYTHON = False

def display_dataframe_to_user(name: str, dataframe: pd.DataFrame) -> None:
    """
    Display a pandas DataFrame to the user with a provided title.

    Parameters:
        name (str): Title for the displayed DataFrame.
        dataframe (pd.DataFrame): The DataFrame to be displayed.
    """
    header = f"\n{name}\n{'=' * len(name)}"
    print(header)
    
    # If running in an IPython environment (like Jupyter Notebook), use HTML rendering.
    if _HAS_IPYTHON:
        display(HTML(dataframe.to_html()))
    else:
        # Fallback: print the DataFrame textually.
        print(dataframe)

# Example usage:
if __name__ == "__main__":
    # Create a sample DataFrame
    sample_data = {
        'Metric': ['A', 'B', 'C'],
        'Value': [10, 20, 30]
    }
    sample_df = pd.DataFrame(sample_data)
    
    # Display the DataFrame with a title.
    display_dataframe_to_user("Sample Data", sample_df)
