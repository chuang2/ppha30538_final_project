selected_variables = [
    # Household Identifier Index
    "hrhhid", "hrhhid2",
    # Frequency and Type of Volunteering
    "pes16", "pes16d", "pts16e",
    # Political Engagement
    "pes2", "pes5", "pes13", "pes14",
    # Civic Participation and Group Membership
    "pes15", "pes15a",
    # Neighbor and Community Interaction
    "pes7",
    # Voting Behavior
    "pes11",
    # Social Media and News Consumption
    "pes9", "pes10",
    # Basic Demographics
    "prtage", "pesex", "ptdtrace", "pemaritl", "hrnumhou", "gestfips",
    # Potential Confounding Variables
    "hefaminc", "peeduca", "gtmetsta", "pes7", "pes9"
]

# Rename the columns
rename_mapping = {
    # Household Identifier Index
    "hrhhid": "Household_ID",
    "hrhhid2": "Household_ID_2",
    # Frequency and Type of Volunteering
    "pes16": "Volunteered_Past_Year",
    "pes16d": "Volunteering_Frequency",
    "pts16e": "Hours_Spent_Volunteering",
    # Political Engagement
    "pes2": "Discussed_Issues_With_Friends_Family",
    "pes5": "Discussed_Issues_With_Neighbors",
    "pes13": "Contacted_Public_Official",
    "pes14": "Boycott_Based_On_Values",
    # Civic Participation and Group Membership
    "pes15": "Belonged_To_Groups",
    "pes15a": "Number_Of_Groups",
    # Neighbor and Community Interaction
    "pes7": "Community_Improvement_Activities",
    # Voting Behavior
    "pes11": "Voted_In_Local_Election",
    # Social Media and News Consumption
    "pes9": "Posted_Views_On_Social_Media",
    "pes10": "Frequency_Of_News_Consumption",
    # Basic Demographics
    "prtage": "Age",
    "pesex": "Gender",
    "ptdtrace": "Race_Ethnicity",
    "pemaritl": "Marital_Status",
    "hrnumhou": "Household_Size",
    "gestfips": "US State",
    # Potential Confounding Variables
    "hefaminc": "Family_Income_Level",
    "peeduca": "Education_Level",
    "gtmetsta": "Urban_Rural_Status"
}