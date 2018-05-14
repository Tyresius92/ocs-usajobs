import config
import requests
import json

#########################
# VARIABLE DECLARATIONS #
#########################

EMPTY_STR = ' '
TAB = '\t'
url = "https://data.usajobs.gov/api/Search" 

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
             "special agent", "security professional" ]

#############
# FUNCTIONS #
#############

def get_scrubbed_job_description():
    qual_summary = str(responses['SearchResult']['SearchResultItems'][i]
                          ['MatchedObjectDescriptor']['QualificationSummary'])

    job_summary = str(responses['SearchResult']['SearchResultItems'][i]
                      ['MatchedObjectDescriptor']['UserArea']
                      ['Details']['JobSummary'])

    job_description = qual_summary + job_summary
    
    job_description = job_description.replace('\n', ' ').replace('\r', '')

    return job_description

def get_job_title():
    job_title = str(responses['SearchResult']['SearchResultItems'][i]
                    ['MatchedObjectDescriptor']['PositionTitle'])

    return job_title

def write_file_headers():
    f.write("Position Title" + TAB +
            "Job Function" + TAB +
            "Organization Name" + TAB +
            "Department Name" + TAB +
            "Position ID" + TAB +
            "Position Schedule" + TAB +
            "Industry" + TAB +
            "Academic Qualification Needed" + TAB +
            "Previous Experience" + TAB +
            "JD Text" + '\n')

def get_org_name():
    org_name = str(responses['SearchResult']['SearchResultItems'][i]
                   ['MatchedObjectDescriptor']['OrganizationName'])
    return org_name

def get_dept_name():
    dept_name = str(responses['SearchResult']['SearchResultItems'][i]
                   ['MatchedObjectDescriptor']['DepartmentName'])
    return dept_name

def get_job_function():
    job_function = str(responses['SearchResult']['SearchResultItems'][i]
                       ['MatchedObjectDescriptor']['JobCategory']
                       [0]['Name'])
    return job_function

def get_academic_qualifications():
    try:
        quals = str(responses['SearchResult']['SearchResultItems'][i]
                    ['MatchedObjectDescriptor']['UserArea']['Details']
                    ['Education'])
    except:
        quals = EMPTY_STR
    return quals

def get_position_ID():
    position_id = str(responses['SearchResult']['SearchResultItems'][i]
                      ['MatchedObjectDescriptor']['PositionID'])

    return position_id

def get_position_url():
    position_url = str(responses['SearchResult']['SearchResultItems'][i]
                       ['MatchedObjectDescriptor']['PositionURI'])

def get_position_schedule():
    position_schedule = str(responses['SearchResult']['SearchResultItems'][i]
                            ['MatchedObjectDescriptor']['PositionSchedule']
                            [0]['Name'])

    return position_schedule

def is_not_part_time():
    position_schedule = str(responses['SearchResult']['SearchResultItems'][i]
                            ['MatchedObjectDescriptor']['PositionSchedule'][0]
                            ['Name'])

    if ('Part' or 'part' or 'PART') in position_schedule:
        return False
    else:
        return True

#############
# MAIN CODE #
#############

f = open("public_sector.tsv", "w")

write_file_headers()

for keyword in range(len(keywords)):

    searchparam = {'PositionTitle': keywords[keyword], 'ResultsPerPage': 500}

    response = requests.get(url, headers=headers, params=searchparam)
    responses = response.json()
    
    print(keywords[keyword] + ": " +
          str(responses['SearchResult']['SearchResultCount']))

    for i in range(responses['SearchResult']['SearchResultCount']):

        # Collect data
        job_title = get_job_title()
        job_description = get_scrubbed_job_description()
        dept_name = get_dept_name()
        org_name = get_org_name()
        job_function = get_job_function()
        quals = get_academic_qualifications()
        position_url = get_position_url()
        position_id = get_position_ID()
        position_schedule = get_position_schedule()

        # Write non-part time jobs to file
        if is_not_part_time():
            f.write(job_title + TAB +
                    job_function + TAB +
                    org_name + TAB +
                    dept_name + TAB +
                    position_id + TAB +
                    position_schedule + TAB + 
                    EMPTY_STR + TAB +
                    quals + TAB +
                    EMPTY_STR + TAB +
                    job_description + '\n')

f.close()
