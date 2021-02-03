import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from data import make_daily_df, make_time_df
from builder import make_table

df = make_daily_df()
totals_df = df["totals_df"]
countries_df = df["countries_df"]

country_df = make_time_df("Korea, South")
global_df = make_time_df()

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap",
]

app = dash.Dash(__name__, external_stylesheets=stylesheets)

bubbles_map = px.scatter_geo(
    data_frame=countries_df,
    locations="Country_Region",
    locationmode="country names",
    color="Confirmed",
    hover_name="Country_Region",
    hover_data={
        "Country_Region": False,
        "Confirmed": ":,",
        "Deaths": ":,",
        "Recovered": ":,",
    },
    size="Confirmed",
    color_continuous_scale=px.colors.sequential.Oryel,
    size_max=20,
    # projection="natural earth",
    title="Confirmed By Country",
    template="plotly_dark",
)
bubbles_map.update_layout(margin=dict(r=0, l=0))

bars_graph = px.bar(
    totals_df,
    x="Condition",
    y="Count",
    color=["Confirmed", "Deaths", "Recovered"],
    hover_name="Condition",
    hover_data={
        "Count": ":,",
        "Condition": False,
    },
    template="plotly_dark",
    title="Total Global Cases",
    labels={"color": "Conditions"},
)
bars_graph.update_layout(
    xaxis=dict(title="Conditions"),
    yaxis=dict(
        title="Counts",
    ),
)
# bars_graph.update_traces(marker_color=["#e74c3c", "#8e44ad", "#27ae60"])

app.layout = html.Div(
    style={
        "fontFamily": "Open Sans, sans-serif",
        "minHeight": "100vh",
        "backgroundColor": "#111111",
        "color": "white",
    },
    children=[
        html.Header(
            style={
                "textAlign": "center",
                "paddingTop": "50px",
                "marginBottom": 100,
            },
            children=[
                html.H1(
                    style={"fontSize": "40px"},
                    children="Covid Dashboard",
                )
            ],
        ),
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "4fr 2fr",
                "gap": 40,
            },
            children=[
                html.Div(
                    children=[dcc.Graph(figure=bubbles_map)],
                ),
                html.Div(
                    children=[
                        make_table(
                            countries_df,
                        )
                    ],
                ),
            ],
        ),
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "2fr 4fr",
                "gap": 40,
            },
            children=[
                html.Div(
                    children=[dcc.Graph(figure=bars_graph)],
                ),
                html.Div(),
            ],
        ),
    ],
)


if __name__ == "__main__":
    app.run_server(debug=True)
