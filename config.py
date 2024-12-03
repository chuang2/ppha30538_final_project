# Note: PRSUPINT = had an interview with subject


def enhance_mapping_dictionary(original_dict):
    '''
    I found out that the data dictionaries don't account for existing qualitative data, so 
    this is a function that will help augment our existing dictionaries to capture the times
    where people ignore the numeric codes and write the qualitative data directly.
    For example, if a column has a bunch of "1", "2, "5", "Female", "Metropolitan", etc., it 
    will convert the numeric codes while keeping the qualitative data.

    This will augment all of the existing dictionaries below rather than having to manually 
    change all of them.
    '''
    enhanced_dict = original_dict.copy()
    special_codes = {'-9', '-3', '-2', '-1', '.', '.u', '.r', '.n', '.d'}
    valid_values = {v for k, v in original_dict.items()
                    if k not in special_codes and v not in {'Missing', 'No Answer', 'Refused', 'Do Not Know', 'Not in Universe'}}

    for value in valid_values:
        enhanced_dict[value.upper()] = value
        enhanced_dict[value] = value
        enhanced_dict[value.lower()] = value

    return enhanced_dict


selected_variables = [
    # Household Identifier Index
    "hrhhid", "hrhhid2",
    # Frequency and Type of Volunteering
    "pes16", "pes16d", "pts16e",
    # Political Engagement
    "pes2", "pes5", "pes13", "pes14",
    # Civic Participation and Group Membership
    "pes15",
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


###
###
def calculate_engagement_score(row):
    """
    We're interested in measuring political engagement (and polarization, which is an imperfect 
    but still useful proxy of political engagement)).
    We create this score using a combination of some of the existing responses above.
    Returns a score between 0-100, where higher scores indicate greater political engagement.

    Weights for different components:
    - Value-based boycotts (30%): Requires strong conviction and tangible action
    - Contacting officials (30%): Requires significant effort and civic engagement
    - Discussion with neighbors (15%): Active interpersonal engagement
    - Social media posting (15%): Public engagement, potentially reaching wider audience
    - News consumption (10%): Passive form of engagement

    Returns None if too many values are missing to calculate a reliable score.

    Note: Since the original version of this function gave a result where 99% of respondents
    had a score of 3 out of 100, we worried that the score calculation is affected by
    multiple missing values (refusals, no answers, do not knows, not in universes, etc.)
    We asked ChatGPT to suggest a remedy, which involved creating a valid_responses metric
    and only count scores if respondents answered a majority of engagement-related questions.
    This removes people who skipped over the engagement questions instead of treating them
    as having an engagement score of 0. 

    (There's an argument to be made that people skipping the questions is itself a sign of
    legitimate low political engagement, but there is also evidence that people may feel
    incentives to camouflage their own beliefs if they feel they will be judged.)
    """
    valid_responses = 0
    total_questions = 5  # boycott, contact official, discussion, social media, news
    score = 0

    # Helper function to convert frequency responses to numerical values
    def frequency_to_score(value):
        if value == 'Basically Every Day':
            return 100
        elif value == 'A Few Times a Week':
            return 80
        elif value == 'A Few Times a Month':
            return 60
        elif value == 'Once a Month':
            return 40
        elif value == 'Less Than Once a Month':
            return 20
        elif value == 'Not at All':
            return 0
        elif value in ['No Answer', 'Refusal', 'Do Not Know', 'Not in Universe', 'Missing']:
            return 0, False
        return 0, False

     # Value-based boycotts (30% of total)
    if row.get('Boycott_Based_On_Values') == 'Yes':
        score += 30
        valid_responses += 1
    elif row.get('Boycott_Based_On_Values') == 'No':
        valid_responses += 1

    # Contacting officials (30% of total)
    if row.get('Contacted_Public_Official') == 'Yes':
        score += 30
        valid_responses += 1
    elif row.get('Contacted_Public_Official') == 'No':
        valid_responses += 1

    # Discussion with neighbors (15% of total)
    freq_score, is_valid = frequency_to_score(
        row.get('Discussed_Issues_With_Neighbors', 'Missing'))
    if is_valid:
        score += (freq_score * 0.15)
        valid_responses += 1

    # Social media posting (15% of total)
    freq_score, is_valid = frequency_to_score(
        row.get('Posted_Views_On_Social_Media', 'Missing'))
    if is_valid:
        score += (freq_score * 0.15)
        valid_responses += 1

    # News consumption (10% of total)
    freq_score, is_valid = frequency_to_score(
        row.get('Frequency_Of_News_Consumption', 'Missing'))
    if is_valid:
        score += (freq_score * 0.10)
        valid_responses += 1

    # Return None if less than 60% of questions have valid responses
    if valid_responses < (total_questions * 0.6):
        return None

    return score


def add_engagement_score(df):
    """
    Add a political engagement score column to the dataframe.
    """
    # Calculate scores
    df['political_engagement_score'] = df.apply(
        calculate_engagement_score, axis=1)

    # Add categorical labels based on score ranges
    def score_to_category(score):
        if score >= 80:
            return "Very High Engagement"
        elif score >= 60:
            return "High Engagement"
        elif score >= 40:
            return "Moderate Engagement"
        elif score >= 20:
            return "Low Engagement"
        else:
            return "Very Low Engagement"

    df['engagement_level'] = df['political_engagement_score'].apply(
        score_to_category)

    return df

###

###


# Default dict - common map values for all variables
default_dict = {
    '-9': 'No Answer',
    '-3': 'Refused',
    '-2': 'Do Not Know',
    '-1': 'Not in Universe',
}

# Renaming pes16 - Volunteered Past Year
# In the past 12 months, did [you/[NAME]] spend any time volunteering for any organization or association?

pes16_dict = {
    '1': 'Yes',
    '2': 'No',
    '-1': 'Not in Universe',
    '-3': 'Refusal',
    '-2': 'Do Not Know',
    '-9': 'No Answer',
    '.u': 'No Answer',
    '.r': 'Refusal',
    '.n': 'Not in Universe',
    '.d': 'Do Not Know',
    'Yes': 'Yes',
    'No': 'No'
}

pes16_dict = enhance_mapping_dictionary(pes16_dict)

# Renaming pes16d - Volunteering Frequency
pes16d_dict = {
    '-9': 'No Answer',
    '-3': 'Refusal',
    '-2': 'Do Not Know',
    '-1': 'Not in Universe',
    '1': 'Basically Every Day',
    '2': 'A Few Times a Week',
    '3': 'A Few Times a Month',
    '4': 'Once a Month',
    '5': 'Less Than Once a Month',
    '6': 'Not at All',
    None: 'Missing'
}

pes16d_dict = enhance_mapping_dictionary(pes16d_dict)

pts16e_dict = default_dict.copy()
for i in range(1, 501):
    pts16e_dict[str(i)] = i


# Renaming pes2 - Discussed Issues with Friends/Family
# [In the past 12 months,] how often did [you/[NAME] discuss political, societal, or local issues with friends or family?
pes2_dict = {
    '1': 'Basically Every Day',
    '2': 'A Few Times a Week',
    '3': 'A Few Times a Month',
    '4': 'Once a Month',
    '5': 'Less Than Once a Month',
    '6': 'Not at All',
    '-1': 'Not in Universe',
    '-3': 'Refusal',
    '-2': 'Do Not Know',
    '-9': 'No Answer',
    '.u': 'No Answer',
    '.r': 'Refusal',
    '.n': 'Not in Universe',
    '.d': 'Do Not Know',
}

pes2_dict = enhance_mapping_dictionary(pes2_dict)
# Renaming pes5 - Discussed Issues with Neighbors
# [In the past 12 months,] how often did [you/[NAME]] discuss political, societal, or local issues with [your/his/her] neighbors?
pes5_dict = {
    '1': 'Basically Every Day',
    '2': 'A Few Times a Week',
    '3': 'A Few Times a Month',
    '4': 'Once a Month',
    '5': 'Less Than Once a Month',
    '6': 'Not at All',
    '-1': 'Not in Universe',
    '-3': 'Refusal',
    '-2': 'Do Not Know',
    '-9': 'No Answer',
    '.u': 'No Answer',
    '.r': 'Refusal',
    '.n': 'Not in Universe',
    '.d': 'Do Not Know',
}

pes5_dict = enhance_mapping_dictionary(pes5_dict)

# Renaming pes13 - Contacted Public Official
# [In the past 12 months,] did [you/[NAME]] contact or visit a public official – at any level of government – to express [your/his/her] opinion?

pes13_dict = {
    '1': 'Yes',
    '2': 'No',
    '-9': 'No Answer',
    '-3': 'Refusal',
    '-2': 'Do Not Know',
    '-1': 'Not in Universe',
    '.u': 'No Answer',
    '.r': 'Refusal',
    '.n': 'Not in Universe',
    '.d': 'Do Not Know',
}

pes13_dict = enhance_mapping_dictionary(pes13_dict)

# Renaming pes14 - Boycott Based on Values
# [In the past 12 months,] Did [you/[NAME]] buy or boycott products or services based on the political values or business practices of that company?
pes14_dict = {
    '1': 'Yes',
    '2': 'No',
    '-9': 'No Answer',
    '-3': 'Refusal',
    '-2': 'Do Not Know',
    '-1': 'Not in Universe',
    '.u': 'No Answer',
    '.r': 'Refusal',
    '.n': 'Not in Universe',
    '.d': 'Do Not Know',
}

pes14_dict = enhance_mapping_dictionary(pes14_dict)

# Renaming pes15 - Belonged to Groups
# [In the past 12 months,] did [you/[NAME]] belong to any groups, organizations, or associations?
pes15_dict = {
    '1': 'Yes',
    '2': 'No',
    '-9': 'No Answer',
    '-3': 'Refusal',
    '-2': 'Do Not Know',
    '-1': 'Not in Universe',
    '.u': 'No Answer',
    '.r': 'Refusal',
    '.n': 'Not in Universe',
    '.d': 'Do Not Know',
}

pes15_dict = enhance_mapping_dictionary(pes15_dict)

# Renaming pes7 - Community Improvement Activities
# [In the past 12 months,] did [you/[NAME]] get together with other people from [your/his/her] neighborhood to do something positive for [your/his/her] neighborhood or the community?
pes7_dict = {
    '1': 'Yes',
    '2': 'No',
    '-9': 'No Answer',
    '-3': 'Refusal',
    '-2': 'Do Not Know',
    '-1': 'Not in Universe',
    '.u': 'No Answer',
    '.r': 'Refusal',
    '.n': 'Not in Universe',
    '.d': 'Do Not Know',
    None: 'Missing',
}

pes7_dict = enhance_mapping_dictionary(pes7_dict)

# Renaming pes11 - Voted in Local Election
# [In the past 12 months,] did [you/[NAME]] vote in the last local elections, such as for mayor or school board?
pes11_dict = {
    '1': 'Yes',
    '2': 'No',
    '-9': 'No Answer',
    '-3': 'Refusal',
    '-2': 'Do Not Know',
    '-1': 'Not in Universe',
    '.u': 'No Answer',
    '.r': 'Refusal',
    '.n': 'Not in Universe',
    '.d': 'Do Not Know',
}

pes11_dict = enhance_mapping_dictionary(pes11_dict)

# Renaming pes9 - Posted Views on Social Media
# [In the past 12 months,] how often did [you/[NAME]] post [your/his/her] views about political, societal, or local issues on the internet or social media?
pes9_dict = {
    '1': 'Basically Every Day',
    '2': 'A Few Times a Week',
    '3': 'A Few Times a Month',
    '4': 'Once a Month',
    '5': 'Less Than Once a Month',
    '6': 'Not at All',
    '-9': 'No Answer',
    '-3': 'Refusal',
    '-2': 'Do Not Know',
    '-1': 'Not in Universe',
    '.u': 'No Answer',
    '.r': 'Refusal',
    '.n': 'Not in Universe',
    '.d': 'Do Not Know',
}

pes9_dict = enhance_mapping_dictionary(pes9_dict)

# Renaming pes10 - Frequency of News Consumption
# [In the past 12 months,] how often did [you/[NAME]] read, watch or listen to news or information about political, societal, or local issues?
pes10_dict = {
    '1': 'Basically Every Day',
    '2': 'A Few Times a Week',
    '3': 'A Few Times a Month',
    '4': 'Once a Month',
    '5': 'Less Than Once a Month',
    '6': 'Not at All',
    '-9': 'No Answer',
    '-3': 'Refusal',
    '-2': 'Do Not Know',
    '-1': 'Not in Universe',
    '.u': 'No Answer',
    '.r': 'Refusal',
    '.n': 'Not in Universe',
    '.d': 'Do Not Know',
}

pes10_dict = enhance_mapping_dictionary(pes10_dict)

# Renaming prtage - Age
prtage_dict = default_dict.copy()
for i in range(1, 80):
    prtage_dict[str(i)] = i
prtage_dict['80'] = '80-84'
prtage_dict['85'] = '85+'
prtage_dict['.'] = 'Missing'

# Renaming pesex - Gender
pesex_dict = {
    '-9': 'No Answer',
    '-3': 'Refused',
    '-2': 'Do Not Know',
    '-1': 'Not in Universe',
    '1': 'Male',
    '2': 'Female',
    '.': 'Missing'
}

pesex_dict = enhance_mapping_dictionary(pesex_dict)

# Renaming ptdtrace - Race/Ethnicity
ptdtrace_dict = {
    '-9': 'No Answer',
    '-3': 'Refused',
    '-2': 'Do Not Know',
    '-1': 'Not in Universe',
    '1': 'White Only',
    '2': 'Black Only',
    '3': 'American Indian/Alaskan Native Only',
    '4': 'Asian Only',
    '5': 'Hawaiian/Pacific Islander Only',
    '6': 'White-Black',
    '7': 'White-American Indian/Alaskan Native',
    '8': 'White-Asian',
    '9': 'White-Hawaiian/Pacific Islander',
    '10': 'Black-American Indian/Alaskan Native',
    '11': 'Black-Asian',
    '12': 'Black-Hawaiian/Pacific Islander',
    '13': 'American Indian/Alaskan Native-Asian',
    '14': 'American Indian/Alaskan Native-Hawaiian/Pacific Islander',
    '15': 'Asian-Hawaiian/Pacific Islander',
    '16': 'White-Black-American Indian/Alaskan Native',
    '17': 'White-Black-Asian',
    '18': 'White-Black-Hawaiian/Pacific Islander',
    '19': 'White-American Indian/Alaskan Native-Asian',
    '20': 'White-American Indian/Alaskan Native-Hawaiian/Pacific Islander',
    '21': 'White-Asian-Hawaiian/Pacific Islander',
    '22': 'Black-American Indian/Alaskan Native-Asian',
    '23': 'White-Black-American Indian/Alaskan Native-Asian',
    '24': 'White-American Indian/Alaskan Native-Asian-Hawaiian/Pacific Islander',
    '25': 'Other 3 Race Combinations',
    '26': 'Other 4 and 5 Race Combinations',
    '.u': 'No Answer',
    '.r': 'Refusal',
    '.n': 'Not in Universe',
    '.d': 'Do Not Know',
}

ptdtrace_dict = enhance_mapping_dictionary(ptdtrace_dict)

# Renaming pemaritl - Marital Status
pemaritl_dict = {
    '-9': 'No Answer',
    '-3': 'Refused',
    '-2': 'Do Not Know',
    '-1': 'Not in Universe',
    '1': 'Married, Spouse Present',
    '2': 'Married, Spouse Absent',
    '3': 'Widowed',
    '4': 'Divorced',
    '5': 'Separated',
    '6': 'Never Married',
    '.': 'Missing',
    '.u': 'No Answer',
    '.r': 'Refusal',
    '.n': 'Not in Universe',
    '.d': 'Do Not Know',
}

pemaritl_dict = enhance_mapping_dictionary(pemaritl_dict)

# Renaming hrnumhou - Household Size
hrnumhou_dict = default_dict.copy()
for i in range(1, 17):
    hrnumhou_dict[str(i)] = i

# Renaming hefaminc - Family Income Level
hefaminc_dict = {
    '-9': 'No Answer',
    '-3': 'Refused',
    '-2': 'Do Not Know',
    '-1': 'Not in Universe',
    '1': 'Less Than $5,000',
    '2': '$5,000 to $7,499',
    '3': '$7,500 to $9,999',
    '4': '$10,000 to $12,499',
    '5': '$12,500 to $14,999',
    '6': '$15,000 to $19,999',
    '7': '$20,000 to $24,999',
    '8': '$25,000 to $29,999',
    '9': '$30,000 to $34,999',
    '10': '$35,000 to $39,999',
    '11': '$40,000 to $49,999',
    '12': '$50,000 to $59,999',
    '13': '$60,000 to $74,999',
    '14': '$75,000 to $99,999',
    '15': '$100,000 to $149,999',
    '16': '$150,000 or More',
    '.': 'Missing',
    '.u': 'No Answer',
    '.r': 'Refusal',
    '.n': 'Not in Universe',
    '.d': 'Do Not Know',
}

hefaminc_dict = enhance_mapping_dictionary(hefaminc_dict)

# Renaming peeduca - Education Level
peeduca_dict = {
    '-9': 'No Answer',
    '-3': 'Refused',
    '-2': 'Do Not Know',
    '-1': 'Not in Universe',
    '31': 'Less Than 1st Grade',
    '32': '1st, 2nd, 3rd, or 4th Grade',
    '33': '5th or 6th Grade',
    '34': '7th or 8th Grade',
    '35': '9th Grade',
    '36': '10th Grade',
    '37': '11th Grade',
    '38': '12th Grade, No Diploma',
    '39': 'High School Graduate',
    '40': 'Some College, No Degree',
    '41': 'Associate Degree, Occupational/Vocational',
    '42': 'Associate Degree, Academic',
    '43': 'Bachelor\'s Degree',
    '44': 'Master\'s Degree',
    '45': 'Professional School Degree',
    '46': 'Doctorate Degree',
    '.': 'Missing',
    '.u': 'No Answer',
    '.r': 'Refusal',
    '.n': 'Not in Universe',
    '.d': 'Do Not Know',
}

peeduca_dict = enhance_mapping_dictionary(peeduca_dict)


# Renaming gtmetsta - Urban/Rural Status
gtmetsta_dict = {
    '-9': 'No Answer',
    '-3': 'Refused',
    '-2': 'Do Not Know',
    '-1': 'Not in Universe',
    '1': 'Metropolitan',
    '2': 'Nonmetropolitan',
    '3': 'Not Identified',
    '.': 'Missing'
}

gtmetsta_dict = enhance_mapping_dictionary(gtmetsta_dict)
