# Note: PRSUPINT = had an interview with subject

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

# Renaming pes15a - Number of Groups
# How many groups, organizations, or associations would you say [you have/[NAME] has] belonged to over the past 12 months?
pes15a_dict = {
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7 or More',
    '-9': 'No Answer',
    '-3': 'Refusal',
    '-2': 'Do Not Know',
    '-1': 'Not in Universe',
    '.u': 'No Answer',
    '.r': 'Refusal',
    '.n': 'Not in Universe',
    '.d': 'Do Not Know',
}

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
}

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

# Renaming prtage - Age
prtage_dict = default_dict.copy()
for i in range(1, 80):
    prtage_dict[str(i)] = i
prtage_dict['80'] = '80-84'
prtage_dict['85'] = '85+'
prtage_dict['.'] = 'Missing'

# Renaming pesex - Gender
pesex_dict = {
    '1': 'Male',
    '2': 'Female',
    '.': 'Missing'
}

# Renaming ptdtrace - Race/Ethnicity
ptdtrace_dict = {
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
    '26': 'Other 4 and 5 Race Combinations'
}

# Renaming pemaritl - Marital Status
pemaritl_dict = {
    '1': 'Married, Spouse Present',
    '2': 'Married, Spouse Absent',
    '3': 'Widowed',
    '4': 'Divorced',
    '5': 'Separated',
    '6': 'Never Married',
    '.': 'Missing'
}

# Renaming hrnumhou - Household Size
hrnumhou_dict = default_dict.copy()
for i in range(1, 17):
    hrnumhou_dict[str(i)] = i

# Renaming hefaminc - Family Income Level
hefaminc_dict = {
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
    '.': 'Missing'
}

# Renaming peeduca - Education Level
peeduca_dict = {
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
    '.': 'Missing'
}

# Renaming gtmetsta - Urban/Rural Status
gtmetsta_dict = {
    '1': 'Metropolitan',
    '2': 'Nonmetropolitan',
    '3': 'Not Identified',
    '.': 'Missing'
}
