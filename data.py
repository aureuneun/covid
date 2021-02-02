import pandas as pd


def make_daily_df():
    daily_df = pd.read_csv("data/daily_report.csv")

    totals_df = (
        daily_df[["Confirmed", "Deaths", "Recovered"]].sum().reset_index(name="Count")
    )
    totals_df = totals_df.rename(columns={"index": "Condition"})

    countries_df = daily_df[["Country_Region", "Confirmed", "Deaths", "Recovered"]]
    countries_df = countries_df.groupby("Country_Region").sum().reset_index()

    return {"totals_df": totals_df, "countries_df": countries_df}


df = make_daily_df()
print(df["totals_df"])
print(df["countries_df"])


conditions = ["confirmed", "deaths", "recovered"]


def make_time_df(country=None):
    def make_df(condition):
        df = pd.read_csv(f"data/time_{condition}.csv")
        if country is not None:
            df = df.loc[df["Country/Region"] == country]
        df = (
            df.drop(columns=["Country/Region", "Lat", "Long"])
            .sum()
            .reset_index(name=condition.capitalize())
        )
        df = df.rename(columns={"index": "Date"})
        return df

    final_df = None
    for condition in conditions:
        condition_df = make_df(condition)
        if final_df is None:
            final_df = condition_df
        else:
            final_df = final_df.merge(condition_df)
    return final_df


df = make_time_df("Korea, South")
print(df)

df = make_time_df()
print(df)
