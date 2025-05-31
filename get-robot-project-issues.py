from jira_util import login
import csv
import datetime

# Construct the hyperlink using OSC 8 escape sequences
def get_hyperlink(url, text):
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"

jira = login()

# Query all issues in the Robot project with pagination
jql_query = 'project = "Robot" ORDER BY key ASC'

# Fetch all issues using pagination
all_issues = []
start_at = 0
max_results = 100  # Use a reasonable page size

print("Fetching issues...")

while True:
    # Get a batch of issues
    issues_batch = jira.search_issues(jql_query, startAt=start_at, maxResults=max_results)

    if not issues_batch:
        break

    all_issues.extend(issues_batch)
    print(f"Fetched {len(all_issues)} issues so far...")

    # If we got fewer results than requested, we've reached the end
    if len(issues_batch) < max_results:
        break

    start_at += max_results

issues = all_issues
print(f"\nFound {len(issues)} total issues in Robot project:\n")

# Create CSV file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
csv_filename = f"robot_project_issues_{timestamp}.csv"

print(f"Creating CSV file: {csv_filename}")

with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    if issues:
        # Get all available field names from the first issue
        sample_issue = issues[0]

        # Define the CSV headers - common fields that are useful
        headers = [
            'Key', 'Summary', 'Status', 'Issue Type', 'Priority', 'Assignee',
            'Reporter', 'Created', 'Updated', 'Due Date', 'Resolution',
            # 'Description', 'Labels', 'Components', 'Fix Versions', 'Affects Versions',
            # 'Story Points', 'Sprint', 'Epic Link', 'Parent', 'Permalink'
        ]

        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        for issue in issues:
            # Helper function to safely get field values
            def safe_get(obj, attr, default=""):
                try:
                    value = getattr(obj, attr, default)
                    return str(value) if value is not None else default
                except:
                    return default

            # Helper function to get list values as comma-separated string
            def get_list_field(field_list, attr="name"):
                if not field_list:
                    return ""
                try:
                    return ", ".join([getattr(item, attr, str(item)) for item in field_list])
                except:
                    return ""

            row = {
                'Key': issue.key,
                'Summary': safe_get(issue.fields, 'summary'),
                'Status': safe_get(issue.fields.status, 'name') if issue.fields.status else "",
                'Issue Type': safe_get(issue.fields.issuetype, 'name') if issue.fields.issuetype else "",
                'Priority': safe_get(issue.fields.priority, 'name') if issue.fields.priority else "",
                'Assignee': safe_get(issue.fields.assignee, 'displayName') if issue.fields.assignee else "Unassigned",
                'Reporter': safe_get(issue.fields.reporter, 'displayName') if issue.fields.reporter else "",
                'Created': safe_get(issue.fields, 'created'),
                'Updated': safe_get(issue.fields, 'updated'),
                'Due Date': safe_get(issue.fields, 'duedate'),
                'Resolution': safe_get(issue.fields.resolution, 'name') if issue.fields.resolution else "",
                #'Description': safe_get(issue.fields, 'description'),
                #'Labels': ", ".join(issue.fields.labels) if issue.fields.labels else "",
                #'Components': get_list_field(issue.fields.components),
                #'Fix Versions': get_list_field(issue.fields.fixVersions),
                #'Affects Versions': get_list_field(issue.fields.versions),
                #'Story Points': safe_get(issue.fields, 'customfield_10016'),  # Common story points field
                #'Sprint': safe_get(issue.fields, 'customfield_10020'),  # Common sprint field
                #'Epic Link': safe_get(issue.fields, 'customfield_10014'),  # Common epic link field
                #'Parent': safe_get(issue.fields.parent, 'key') if hasattr(issue.fields, 'parent') and issue.fields.parent else "",
                #'Permalink': issue.permalink()
            }

            writer.writerow(row)

print(f"CSV file created: {csv_filename}")
print(f"Exported {len(issues)} issues to CSV\n")

# Pretty print result
key_width = 15
status_width = 15
assignee_width = 20

for issue in issues:
    key = get_hyperlink(issue.permalink(), issue.key).ljust(key_width)
    summary = issue.fields.summary
    status = f"{issue.fields.status.name}".ljust(status_width)
    assignee = (issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned").ljust(assignee_width)
    print(f"{key}: {status} {assignee} {summary}")
