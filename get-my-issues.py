from jira_util import login

# Construct the hyperlink using OSC 8 escape sequences
def get_hyperlink(url, text):
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"

jira = login()

# Query issues assigned to user
jql_query = 'assignee = currentUser() ORDER BY priority DESC'
issues = jira.search_issues(jql_query, maxResults=1000)


# Order issues by status name
status_order = {
    "BACKLOG": 0,
    "TO DO": 1,
    "IN PROGRESS": 2,
    "MERGED": 3,
    "QA": 4,
    "DONE": 5,
    "REJECTED": 6
}
issues = sorted(issues, key=lambda issue: issue.fields.status.id)


# Pretty print result
key_width = 15
status_width = 15

for issue in issues:
    key = get_hyperlink(issue.permalink(), issue.key).ljust(key_width)
    summary = issue.fields.summary
    status = f"{issue.fields.status.name}".ljust(status_width)
    print(f"{key}: {status} {summary}")
