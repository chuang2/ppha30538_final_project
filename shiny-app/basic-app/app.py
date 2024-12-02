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

variable_mapping = {
    "Family_Income_Level": "Household Income",
    "Education_Level": "Education Level",
    "Urban_Rural_Status": "Urban/Rural Status",
    "Community_Improvement_Activities": "Community Involvement",
    "Posted_Views_On_Social_Media": "Social Media Use"
}


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
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select(
                "variable",
                "Select Variable to Analyze",
                choices=list(variable_mapping.values())
            ),
            ui.input_checkbox(
                "sort_bars",
                "Sort bars by volunteering rates",
                value=False
            )
        ),
        ui.div(
            output_widget("volunteer_plot"),
            style="margin-bottom: 100px;"  # Add significant margin below the plot
        ),
        ui.div(
            ui.output_text("exclusion_stats_output"),
            style="padding: 20px 0;"  # Add padding above and below the stats
        )
    )
)


def server(input, output, session):

    # Helper function to get column name from display name
    def get_column_name(display_name):
        return {v: k for k, v in variable_mapping.items()}[display_name]

    @output
    @render.text
    def variable_description():
        selected_var = input.variable()
        descriptions = {
            "Household Income": "Analysis of volunteering rates across different household income levels",
            "Education Level": "Analysis of volunteering rates by educational attainment",
            "Urban/Rural Status": "Comparison of volunteering rates between urban and rural areas",
            "Community Involvement": "Volunteering rates by level of community participation",
            "Social Media Use": "Volunteering rates by social media engagement level"
        }
        return descriptions[selected_var]

    @output
    @render_altair
    def volunteer_plot():
        selected_column = get_column_name(input.variable())

        filtered_data = cev_all_2021_filter[~cev_all_2021_filter[selected_column].isin(
            exclude_categories)]

        volunteer_data = (filtered_data
                          .groupby(selected_column)['Volunteered_Past_Year']
                          .agg(lambda x: (x == "Yes").mean() * 100)
                          .reset_index()
                          .rename(columns={
                              selected_column: input.variable(),
                              'Volunteered_Past_Year': 'Volunteer_Rate'})
                          )
        # Sort if requested
        if input.sort_bars():
            volunteer_data = volunteer_data.sort_values(
                'Volunteer_Rate', ascending=False)

        # Chart creation also needs to be indented
        chart = alt.Chart(volunteer_data).mark_bar().encode(
            x=alt.X(input.variable(), title=input.variable(),
                    sort=alt.EncodingSortField(
                    field='Volunteer_Rate',
                    order='descending'
                    ) if input.sort_bars() else None),
            y=alt.Y('Volunteer_Rate', title="Percentage Volunteered"),
            tooltip=[
                alt.Tooltip(input.variable()),
                alt.Tooltip('Volunteer_Rate',
                            title='Volunteer Rate (%)', format='.1f')
            ]
        ).properties(
            title=f"Volunteering Rates by {input.variable()}",
            width=600,
            height=300
        )
        return chart

    @output
    @render.text
    def exclusion_stats_output():
        return calculate_exclusion_stats("Education_Level")


app = App(app_ui, server)
