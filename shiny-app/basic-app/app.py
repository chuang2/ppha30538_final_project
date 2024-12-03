from shiny import App, render, ui, reactive
from shinywidgets import render_altair, output_widget
import pandas as pd
import altair as alt

from pathlib import Path


# Load dataset from data folder
data_path = Path("data/cev_2021_cleaned.csv")
cev_all_2021_filter = pd.read_csv(data_path)

### Base definitions/functions used for all apps below##

exclude_categories = ['No Answer', 'Refused', 'Do Not Know', 'Not in Universe']

variable_mapping = {
    "Household_Size": "Household Size",
    "US State": "US State",
    "Family_Income_Level": "Family Income",
    "Education_Level": "Education Level",
    "Urban_Rural_Status": "Urban/Rural Status",
    "Community_Improvement_Activities": "Community Involvement",
    "Posted_Views_On_Social_Media": "Social Media Use",
    "Age": "Age",
    "Gender": "Gender",
    "Race_Ethnicity": "Race/Ethnicity",
    "Marital_Status": "Marital Status"
}


def calculate_exclusion_stats(category):
    '''
    Counts the number and proportion of responses that turn up 
    '''
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
            style="margin-bottom: 100px;"
        ),
        ui.div(
            ui.output_text("exclusion_stats_output"),
            # Add padding above and below the stats so this doesn't get covered up
            style="padding: 20px 0;"
        )
    )
)


def server(input, output, session):

    def get_column_name(display_name):
        '''
        Helper function to get column name from display name
        '''
        return {v: k for k, v in variable_mapping.items()}[display_name]

    @reactive.Calc
    def processed_data():
        """
        processes the data and picks the category based on whatever the user selects
        adds binning if the user selects "age" as a category
        """
        selected_column = get_column_name(input.variable())

        # Attribution: ChatGPT
        # Asked "how to bin age-related data using pandas for easier bar-graphing", suggested using pd.cut()
        if selected_column == "Age":
            numeric_age = pd.to_numeric(
                cev_all_2021_filter['Age'], errors='coerce')

            age_groups = pd.cut(
                numeric_age,
                bins=[0, 25, 35, 45, 55, 65, 100],
                labels=['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
            )
            return cev_all_2021_filter.assign(Age=age_groups)

        return cev_all_2021_filter

    @output
    @render.text
    def variable_description():
        selected_var = input.variable()
        descriptions = {
            "Household Income": "Analysis of volunteering rates across different household income levels",
            "Education Level": "Analysis of volunteering rates by educational attainment",
            "Urban/Rural Status": "Comparison of volunteering rates between urban and rural areas",
            "Community Involvement": "Volunteering rates by level of community participation",
            "Social Media Use": "Volunteering rates by social media engagement level",
            "Age": "Analysis of volunteering rates by age group",
            "Gender": "Analysis of volunteering rates by gender",
            "Race/Ethnicity": "Analysis of volunteering rates by race and ethnicity",
            "Marital Status": "Analysis of volunteering rates by marital status"

        }
        return descriptions[selected_var]

    @output
    @render_altair
    def volunteer_plot():
        # Get processed data with any special handling (like age groups)
        data = processed_data()
        selected_column = get_column_name(input.variable())

        filtered_data = data[~data[selected_column].isin(exclude_categories)]

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
                    ) if input.sort_bars() else None,
                    axis=alt.Axis(labelAngle=45)),
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
        return calculate_exclusion_stats(get_column_name(input.variable()))


app = App(app_ui, server)
