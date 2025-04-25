from jira_util import login

jira = login()

issue_dict = {
    'project': {'key': 'FW'},
    'summary': 'Test issue',
    'description': 'This is a test issue',
    'issuetype': {'id': 5}
}

try:
    new_issue = jira.create_issue(fields=issue_dict)
    print(f"New issue created: {new_issue}")
except Exception as e:
    print(f"Failed to create issue: {e}")
