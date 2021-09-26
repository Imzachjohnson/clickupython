from clickupython import client

"""
	Here's how to validate a personal API key and create a new task with a 
    due date. When creating a new task, the only required arguments are list_id and name. 
    Name will be the title of your list on ClickUp.
"""


c = client.ClickUpClient("YOUR_API_KEY")
t = c.create_task("LIST_ID", name="Test Task", due_date="march 2 2021")


"""
	Here's two ways to get all the comments for a given task ID.
"""

# Example 1
c = client.ClickUpClient("YOUR_API_KEY")
comments = c.get_task_comments("TASK_ID")

for comment in comments:
    print(comment.user.id)
    print(comment.comment_text)

# Example 2
c = client.ClickUpClient("YOUR_API_KEY")
task = c.get_task("TASK_ID")
comments = task.get_comments(c)

for comment in comments:
    print(comment.comment_text)


"""
	Here how to get all teams on an account. Teams is the legacy term for what are now called Workspaces in ClickUp. 
    For compatibility, the term team is still used in the API. This is NOT the new "Teams" feature which represents a group of users.
"""
c = client.ClickUpClient("YOUR_API_KEY")
teams = c.get_teams()
for team in teams:
    print(team.name)

"""
	Here's two ways to create a checklist and add checklist items to it.
"""

# Example 1
c = client.ClickUpClient("YOUR_API_KEY")
checklist = c.create_checklist("TASK_ID", "Test Checklist")
checklist_with_item = c.create_checklist_item(checklist.id, "Test Checklist item")

# Example 2
c = client.ClickUpClient("YOUR_API_KEY")
checklist = c.create_checklist("1gu4f5g", "Test Checklist")

item_list = ["Item1", "Item2", "Item3"]

for item in item_list:
    checklist.add_item(c, item)
