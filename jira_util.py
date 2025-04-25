import dotenv
import os
import jira

def login():
    # Load environment variables
    dotenv.load_dotenv()
    JIRA_SERVER = os.getenv('JIRA_SERVER')
    JIRA_USERNAME = os.getenv('JIRA_USERNAME')
    JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
    # Log in to Jira
    j = jira.JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USERNAME, JIRA_API_TOKEN))
    myself = j.myself()
    print(f"Logged in as: {myself['displayName']} ({myself['emailAddress']})")
    return j
