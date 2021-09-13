from clickupy import client

'''
	Here's how to validate a personal API key and create a new task with a 
    due date. When creating a new task, the only required arguments are list_id and name. 
    Name will be the title of your list on ClickUp.
'''


c = client.ClickUpClient("YOUR_API_KEY")
t = c.create_task("LIST_ID", name="Test Task", due_date="march 2 2021")


'''
	Here's how to get all the comments for a given task ID.
'''


c = client.ClickUpClient("YOUR_API_KEY")
comments = c.get_task_comments("TASK_ID")

for c in comments:
    print(c.user.id)
    print(c.comment_text)
