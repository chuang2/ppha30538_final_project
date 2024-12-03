from shiny import App, render, ui, reactive
from shinywidgets import render_altair, output_widget
import pandas as pd
import altair as alt

from pathlib import Path


# Load dataset from data folder
data_path = Path("data/cev_2021_cleaned.csv")
cev_all_2021_filter = pd.read_csv(data_path, low_memory=False)

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


def calculate_exclusion_stats(category, metric_type=None):
    '''
    Counts the number and proportion of responses that are exclusded, nonresponse, or out of universe, etc.
    '''

    data = cev_all_2021_filter.copy()

    excluded_category = data[data[category].isin(exclude_categories)]

    # For engagement score, also count insufficient data
    if metric_type == "engagement":
        excluded_engagement = data[pd.isna(data['political_engagement_score'])]
        excluded = pd.concat(
            [excluded_category, excluded_engagement]).drop_duplicates()
    else:
        excluded = excluded_category

    total_count = len(data)
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
            ui.input_select(
                "metric",
                "Select Metric",
                choices={
                    "volunteer": "Volunteering Rates",
                    "engagement": "Political Engagement Score"
                }
            ),
            ui.input_checkbox(
                "sort_bars",
                "Sort bars by selected metric",
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
        Helper function to get column name from display name dict
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
        metric_type = input.metric()

        filtered_data = data[~data[selected_column].isin(exclude_categories)]

        if metric_type == "volunteer":

            metric_data = (filtered_data
                           .groupby(selected_column)['Volunteered_Past_Year']
                           .agg(lambda x: (x == "Yes").mean() * 100)
                           .reset_index()
                           .rename(columns={
                               selected_column: input.variable(),
                               'Volunteered_Past_Year': 'Metric_Value'})
                           )

            y_title = "Percentage Volunteered"
            tooltip_title = "Volunteer Rate (%)"

        else:
            # Engagement score calculation
            metric_data = (filtered_data
                           .groupby(selected_column)['political_engagement_score']
                           .mean()
                           .reset_index()
                           .rename(columns={
                               selected_column: input.variable(),
                               'political_engagement_score': 'Metric_Value'})
                           )
            y_title = "Average Political Engagement Score"
            tooltip_title = "Engagement Score"

        # Debugging - handle empty data - suggested by ChatGPT
        if metric_data.empty:
            print(f"No data available for {input.variable()}.")
            return alt.Chart(pd.DataFrame({'No Data': [1]})).mark_text(
                text="No data available"
            ).encode()

        # Sort if requested
        if input.sort_bars():
            metric_data = metric_data.sort_values(
                'Metric_Value', ascending=False)

        chart = alt.Chart(metric_data).mark_bar().encode(
            x=alt.X(input.variable(), title=input.variable(),
                    sort=alt.EncodingSortField(
                    field='Metric_Value',
                    order='descending'
                    ) if input.sort_bars() else None,
                    axis=alt.Axis(labelAngle=45)),
            y=alt.Y('Metric_Value', title=y_title),
            tooltip=[
                alt.Tooltip(input.variable()),
                alt.Tooltip('Metric_Value',
                            title=tooltip_title, format='.1f')
            ]
        ).properties(
            title=f"{y_title} by {input.variable()}",
            width=600,
            height=300
        )

        return chart

    @output
    @render.text
    def exclusion_stats_output():
        selected_column = get_column_name(input.variable())
        metric_type = input.metric()
        return calculate_exclusion_stats(selected_column, metric_type)


app = App(app_ui, server)
