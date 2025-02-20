import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


class PlotUtils:
    """Utility class for creating modular plots in Streamlit."""

    @staticmethod
    def generate_sample_data(n=100):
        """Generate sample data for testing."""
        np.random.seed(42)
        df = pd.DataFrame({
            "category": np.random.choice(["A", "B", "C", "D"], n),
            "value": np.random.randint(10, 100, n),
            "date": pd.date_range(start="2023-01-01", periods=n, freq="D"),
            "x": np.random.randn(n),
            "y": np.random.randn(n),
        })
        return df

    @staticmethod
    def plot_bar_chart(df=None, x_col="category", y_col="value"):
        """Plot a bar chart with default or provided data."""
        if df is None:
            df = PlotUtils.generate_sample_data()
        fig = px.bar(df, x=x_col, y=y_col, title="Bar Chart", color=x_col)
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def plot_line_chart(df=None, x_col="date", y_col="value"):
        """Plot a line chart with default or provided data."""
        if df is None:
            df = PlotUtils.generate_sample_data()
        fig = px.line(df, x=x_col, y=y_col, title="Line Chart")
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def plot_scatter_chart(df=None, x_col="x", y_col="y"):
        """Plot a scatter chart with default or provided data."""
        if df is None:
            df = PlotUtils.generate_sample_data()
        fig = px.scatter(df, x=x_col, y=y_col, color="category", title="Scatter Plot")
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def plot_pie_chart(df=None, category_col="category", value_col="value"):
        """Plot a pie chart with default or provided data."""
        if df is None:
            df = PlotUtils.generate_sample_data()
        fig = px.pie(df, names=category_col, values=value_col, title="Pie Chart")
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def plot_histogram(df=None, x_col="value"):
        """Plot a histogram with default or provided data."""
        if df is None:
            df = PlotUtils.generate_sample_data()
        fig = px.histogram(df, x=x_col, title="Histogram", nbins=20)
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def plot_box_plot(df=None, x_col="category", y_col="value"):
        """Plot a box plot with default or provided data."""
        if df is None:
            df = PlotUtils.generate_sample_data()
        fig = px.box(df, x=x_col, y=y_col, title="Box Plot")
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def plot_heatmap(df=None):
        """Plot a heatmap using Seaborn with default or provided data."""
        if df is None:
            df = PlotUtils.generate_sample_data(50)
        corr_matrix = df[["x", "y", "value"]].corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)


