from shiny import App, render, ui
from shinywidgets import render_altair, output_widget
import pandas as pd
import altair as alt

import os
from pathlib import Path


# Load dataset from data folder
data_path = Path("data/cev_2021_cleaned.csv")
cev_all_2021_filter = pd.read_csv(data_path)

### Base definitions/functions used for all apps below##

exclude_categories = ['No Answer', 'Refused', 'Do Not Know', 'Not in Universe']


def calculate_exclusion_stats(category):
    excluded = cev_all_2021_filter[
        cev_all_2021_filter[category].isin(exclude_categories)]
    total_count = len(cev_all_2021_filter)
    excluded_count = len(excluded)
    excluded_percent = (excluded_count / total_count) * 100

    return (f"Number of responses excluded: {excluded_count:,} out of {total_count:,}\n\n || "
            f"Percentage of total responses excluded: {excluded_percent:.1f}%")

###


app_ui = ui.page_fluid(
    ui.panel_title("Civic Engagement Analysis Dashboard"),
    output_widget("education_plot"),
    ui.output_text("exclusion_stats_output")
)


def server(input, output, session):
    @output
    @render_altair
    def education_plot():
        category = "Education_Level"
        filtered_data = cev_all_2021_filter[~cev_all_2021_filter['Education_Level'].isin(
            exclude_categories)]
        volunteer_data = (filtered_data
                          .groupby("Education_Level")['Volunteered_Past_Year']
                          .agg(lambda x: (x == "Yes").mean() * 100)
                          .reset_index()
                          .rename(columns={'Volunteered_Past_Year': 'Volunteer_Rate'})
                          )

        # Chart creation also needs to be indented
        chart = alt.Chart(volunteer_data).mark_bar().encode(
            x=alt.X('Education_Level'),
            y=alt.Y('Volunteer_Rate', title="Percentage Volunteered")
        )
        return chart

    @output
    @render.text
    def exclusion_stats_output():
        return calculate_exclusion_stats("Education_Level")


app = App(app_ui, server)
