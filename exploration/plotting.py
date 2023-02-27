import datetime as dt
import pandas as pd
import plotly.graph_objects as go


class CandlePlot:
    def __init__(self, df):
        self.fig = None
        self.df_plot = df.copy()
        self.create_candlestick_chart()

    def add_timestr(self):
        self.df_plot['sTime'] = [dt.datetime.strftime(x, "s%y-%m-%d %H:%M") for x in self.df_plot.time]

    def create_candlestick_chart(self):
        """
        Create a candlestick chart using Plotly.

        Requires the following columns in the self.df_plot DataFrame:
        - time
        - mid_o
        - mid_h
        - mid_l
        - mid_c
        """
        # Validate input
        if "sTime" not in self.df_plot.columns or \
                "mid_o" not in self.df_plot.columns or "mid_h" \
                not in self.df_plot.columns or \
                "mid_l" not in self.df_plot.columns or "mid_c" not in self.df_plot.columns:
            raise ValueError("self.df_plot must contain columns 'sTime', 'mid_o', 'mid_h', 'mid_l', and 'mid_c'")

        # Add time string column
        self.add_timestr()

        # Create the candlestick chart
        chart_style = {
            'line': {'width': 1},
            'opacity': 1,
            'increasing': {'fillcolor': '#24A06B', 'line_color': '#2EC886'},
            'decreasing': {'fillcolor': '#CC2E3C', 'line_color': '#FF3A4C'}
        }

        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=self.df_plot.sTime,
            open=self.df_plot.mid_o,
            high=self.df_plot.mid_h,
            low=self.df_plot.mid_l,
            close=self.df_plot.mid_c,
            **chart_style
        ))

        # assign the created figure to self.fig
        self.fig = fig

    def update_layout(self, figure_width, figure_height, xaxis_nticks):
        """
        Update the layout of the Plotly figure object.

        Parameters:
        - figure_width: integer, width of the figure in pixels
        - figure_height: integer, height of the figure in pixels
        - xaxis_nticks: integer, number of ticks on the x-axis
        """
        # Validate input
        if not isinstance(figure_width, int) or figure_width <= 0:
            raise ValueError("figure_width must be a positive integer")

        if not isinstance(figure_height, int) or figure_height <= 0:
            raise ValueError("figure_height must be a positive integer")

        # Update y-axis settings
        self.fig.update_yaxes(gridcolor="#1f292f")

        # Update x-axis settings
        self.fig.update_xaxes(
            gridcolor="#1f292f",
            rangeslider=dict(visible=False),
            nticks=xaxis_nticks
        )

        # Define layout settings
        layout_settings = {
            'width': figure_width,
            'height': figure_height,
            'margin': dict(l=10, r=10, b=10, t=10),
            'paper_bgcolor': "#2c303c",
            'plot_bgcolor': "#2c303c",
            'font': dict(size=8, color="#e1e1e1")
        }

        # Update layout with settings
        self.fig.update_layout(layout_settings)

    def show_plot(self, figure_width=1500, figure_height=400, xaxis_nticks=5):
        """
        Update the layout of the Plotly figure object and display the plot.

        Parameters:
        - figure_width: integer, width of the figure in pixels (default: 1500)
        - figure_height: integer, height of the figure in pixels (default: 400)
        - xaxis_nticks: integer, number of ticks on the x-axis (default: 5)
        """
        # Validate input
        if not isinstance(figure_width, int) or figure_width <= 0:
            raise ValueError("figure_width must be a positive integer")

        if not isinstance(figure_height, int) or figure_height <= 0:
            raise ValueError("figure_height must be a positive integer")

        # Update layout if necessary
        if figure_width is not None and figure_height is not None and xaxis_nticks is not None:
            self.update_layout(figure_width, figure_height, xaxis_nticks)

        # Show plot
        self.fig.show()
