from clickupy import client

'''
	Here's how to validate a personal API key and create a new task with a 
    due date. When creating a new task, the only required arguments are list_id and name. 
    Name will be the title of your list on ClickUp.
'''


c = client.ClickUpClient("pk_6341704_8OV9MRRLXIK2VO3XV3FNKKLY9IMQAXB3")
t = c.create_task("132216026", name="Test task", due_date="march 2 2021")
