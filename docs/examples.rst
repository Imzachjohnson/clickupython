Examples
====================================
Clickupy is a Python client for the ClickUp API and can be used to interact with the ClickUp API in your projects. ClickUp's API exposes the entire ClickUp infrastructure via a standardized programmatic interface. Using ClickUp's API, you can do just about anything you can do on clickup.com.


Tasks
*****

Creating a Task
---------------
Here's how to create a new ClickupClient instance and validate a personal API key with the ClickUp API and create a new task with a 
due date. When creating a new task, the only required arguments are list_id and name. Name will be the title of your list on ClickUp.

Example::

   c = client.ClickUpClient("YOUR_API_KEY")
   t = c.create_task("LIST_ID", name="Test Task", due_date="march 2 2021")


Fetching all Tasks from a List
---------------

You can quickly get all tasks for a given list via the list id:

Example::

   c = client.ClickUpClient("YOUR_API_KEY")
   result = c.get_tasks("list_id")