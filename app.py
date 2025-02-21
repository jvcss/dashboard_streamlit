import streamlit as st
from utils.config import Config
from utils.plot_utils import PlotUtils

st.set_page_config(page_title="Dash Nibo", page_icon=":shark:", layout="wide")

def main():
    st.sidebar(title="Dash Nibo")
    st.sidebar.write("This is a simple example of a Streamlit app.")
    st.sidebar.write("You can use the buttons below to visualize different types of plots.")

    st.title("Dash Nibo")
    st.write("This is a simple example of a Streamlit app.")

    # Fetch database config
    # db_config = Config.get_database_config()
    # st.write(f"Connected to database: {db_config['database']} at {db_config['host']}")

    # Example of fetching a token
    # token_example = Config.get_token("Tk_B2BF")
    # st.write(f"Example Token (Tk_B2BF): {token_example}")

    # Example Usage
    if st.button("Show Bar Chart"):
        PlotUtils.plot_bar_chart()

    if st.button("Show Line Chart"):
        PlotUtils.plot_line_chart()

    if st.button("Show Scatter Plot"):
        PlotUtils.plot_scatter_chart()

    if st.button("Show Pie Chart"):
        PlotUtils.plot_pie_chart()

    if st.button("Show Histogram"):
        PlotUtils.plot_histogram()

    if st.button("Show Box Plot"):
        PlotUtils.plot_box_plot()

    if st.button("Show Heatmap"):
        PlotUtils.plot_heatmap()


if __name__ == "__main__":
    main()