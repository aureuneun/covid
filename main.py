import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from data import make_daily_df, make_time_df
from builder import make_table

df = make_daily_df()
totals_df = df["totals_df"]
countries_df = df["countries_df"]

dropdown_options = countries_df.sort_values("Country_Region").reset_index()
dropdown_options = dropdown_options["Country_Region"]

country_df = make_time_df("Korea, South")
global_df = make_time_df()

stylesheets = [
    "https://cdn.jsdelivr.net/npm/reset-css@5.0.1/reset.min.css",
    "https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap",
]

app = dash.Dash(__name__, external_stylesheets=stylesheets)

app.title = "Covid Dashboard"

server = app.server

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
bubbles_map.update_layout(
    margin=dict(r=0, l=0, b=0), coloraxis_colorbar=dict(xanchor="left", x=0)
)

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
    labels={"color": "Condition"},
)
bars_graph.update_layout(
    xaxis=dict(title="Condition"),
    yaxis=dict(
        title="Count",
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
                html.Div(
                    children=[
                        dcc.Dropdown(
                            id="input",
                            style={
                                "width": 320,
                                "margin": "0 auto",
                                "color": "#111111",
                            },
                            options=[
                                {"label": option, "value": option}
                                for option in dropdown_options
                            ],
                        ),
                        dcc.Graph(id="output"),
                    ]
                ),
            ],
        ),
    ],
)


@app.callback(
    Output("output", "figure"),
    [
        Input(
            "input",
            "value",
        )
    ],
)
def hello(value):
    df = make_time_df(value)
    figure = px.line(
        df,
        x="Date",
        y=["Confirmed", "Deaths", "Recovered"],
        template="plotly_dark",
        hover_data={
            "value": ":,",
            "Date": False,
            "variable": False,
        },
        labels={"value": "Cases", "variable": "Condition"},
    )
    return figure
