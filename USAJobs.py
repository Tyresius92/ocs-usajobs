import config
import requests
import json

#########################
# VARIABLE DECLARATIONS #
#########################

EMPTY_STR = ' '
TAB = '\t'
URL = "https://data.usajobs.gov/api/Search"
MIN_ACCEPTABLE_GRADE = 8
MAX_ACCEPTABLE_GRADE = 12

headers = {
    'authorization-key': config.authorization_key,
    'user-agent': config.user_agent,
    'host': 'data.usajobs.gov',
    'cache-control': 'no-cache'
    }

keywords = [ "budget", "desk", "financial",
             "community outreach", "congressional affairs",
             "counterintelligence threat", "counterterrorism",
             "cyber exploitation", "cyber threat",
             "cybersecurity", "economic",
             "economic research", "education training",
             "financial program", "foreign language",
             "imagery intelligence", "import policy",
             "intelligence", "intelligence collection",
             "intelligence operations", "international relations",
             "international trade compliance", "legislative",
             "logistics management", "management", "operations",
             "passport", "policy", "political", "program",
             "program management", "public affairs",
             "public information", "research", "resource",
             "science technology weapons", "security", "supply",
             "supply chain", "targeting", "foreign service officer",
             "special agent", "security professional", "department of state",
             "usaid", "department of commerce", "treasury", "ustr", "cia",
             "fbi", "defense intelligence agency", "dhs",
             "library of congress" ]

#############
# FUNCTIONS #
#############

def write_file_headers():
    f.write("Position Title" + TAB +
            "Job Function" + TAB +
            "Organization Name" + TAB +
            "Department Name" + TAB +
            "Position ID" + TAB +
            "Position Schedule" + TAB +
            "Low Grade" + TAB +
            "High Grade" + TAB +
            "Industry" + TAB +  # Legacy column
            "Academic Qualification Needed" + TAB +
            "Previous Experience" + TAB + # Legacy Column
            "JD Text" + '\n')

def get_scrubbed_job_description():
    qual_summary = str(curr_job['QualificationSummary'])
    job_summary = str(curr_job['UserArea']['Details']['JobSummary'])

    job_description = qual_summary + job_summary
    job_description = job_description.replace('\n', ' ').replace('\r', '')
    return job_description

def get_job_title():
    job_title = str(curr_job['PositionTitle'])
    return job_title

def get_org_name():
    org_name = str(curr_job['OrganizationName'])
    return org_name

def get_dept_name():
    dept_name = str(curr_job['DepartmentName'])
    return dept_name

def get_job_function():
    job_function = str(curr_job['JobCategory'][0]['Name'])
    return job_function

def get_academic_qualifications():
    try:
        quals = str(curr_job['UserArea']['Details']['Education'])
    except:
        quals = EMPTY_STR
    return quals

def get_position_ID():
    position_id = str(curr_job['PositionID'])
    return position_id

def get_position_url():
    position_url = str(curr_job['PositionURI'])
    return position_url

def get_position_schedule():
    position_schedule = str(curr_job['PositionSchedule'][0]['Name'])
    return position_schedule

def is_part_time():
    position_schedule = str(curr_job['PositionSchedule'][0]['Name'])

    if ('Part' or 'part' or 'PART') in position_schedule:
        return True
    else:
        return False

def get_grade_low():
    low_grade = int(curr_job['UserArea']['Details']['LowGrade'])
    return low_grade

def get_grade_high():
    high_grade = int(curr_job['UserArea']['Details']['HighGrade'])
    return high_grade

def is_outside_grade_range():
    if get_grade_high() < MIN_ACCEPTABLE_GRADE:
        return True
    if get_grade_low() > MAX_ACCEPTABLE_GRADE:
        return True
    return False

def job_meets_criteria():
    try: 
        if is_part_time():
            return False
        if is_outside_grade_range():
            return False
        return True
    except:
        return False

#############
# MAIN CODE #
#############

f = open("public_sector.tsv", "w")

write_file_headers()

for keyword in keywords:

    searchparam = {'Keyword': keyword, 'ResultsPerPage': 500}

    response = requests.get(URL, headers=headers, params=searchparam)
    responses = response.json()
    
    print(keyword + ": " + str(responses['SearchResult']['SearchResultCount']))

    for i in range(responses['SearchResult']['SearchResultCount']):

        curr_job = responses['SearchResult']['SearchResultItems'][i]['MatchedObjectDescriptor']

        if job_meets_criteria(): 

            # Collect data
            job_title = get_job_title()
            job_function = get_job_function()
            org_name = get_org_name()
            dept_name = get_dept_name()
            position_id = get_position_ID()
            position_schedule = get_position_schedule()
            low_grade = str(get_grade_low())
            high_grade = str(get_grade_high())
            job_description = get_scrubbed_job_description()
            quals = get_academic_qualifications()
            position_url = get_position_url()

            # Write to file
            f.write(job_title + TAB +
                    job_function + TAB +
                    org_name + TAB +
                    dept_name + TAB +
                    position_id + TAB +
                    position_schedule + TAB +
                    low_grade + TAB +
                    high_grade + TAB + 
                    EMPTY_STR + TAB +  # Legacy Column - Industry
                    quals + TAB +
                    EMPTY_STR + TAB +  # Legacy Column - Prev Exp
                    job_description + '\n')

f.close()
