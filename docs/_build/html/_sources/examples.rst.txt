Examples
====================================
Clickupy is a Python client for the ClickUp API and can be used to interact with the ClickUp API in your projects. Below are some examples to get you started with clickupy.


Tasks
*****
.. autoclass:: clickupy.models.Task
    :members:
    :undoc-members:
    :show-inheritance:
|
|
.. raw:: html

   <hr>

Creating a Task
---------------
Here's how to create a new ClickupClient instance and validate a personal API key with the ClickUp API and create a new task with a 
due date. When creating a new task, the only required arguments are list_id and name. Name will be the title of your list on ClickUp.

Example::

   c = client.ClickUpClient("YOUR_API_KEY")
   t = c.create_task("LIST_ID", name="Test Task", due_date="march 2 2021")


Fetching a Single Task
---------------
Example: Lookup via ClickUpClient::

   c = client.ClickUpClient("YOUR_API_KEY")
   task = c.get_task(task_id)

   print(task.name)


Fetching all Tasks from a List
---------------
You can quickly get all tasks for a given list via the list id:

Example::

   c = client.ClickUpClient("YOUR_API_KEY")
   tasks = c.get_tasks("list_id")



Filtering Tasks
---------------
Example::

   c = client.ClickUpClient("YOUR_API_KEY")
   tasks = c.get_tasks("list_id", date_updated_gt="august 1 2021", 
          assignees=["4523","4562","5871"], include_closed=True)


This example will return all tasks that have been updated after August 1st, 2021 and are assigned to users with the ids of 4523, 4562, and 5871.
This request will also include tasks that have been marked as "closed."

Example::

   c = client.ClickUpClient("YOUR_API_KEY")
   tasks = c.get_tasks("list_id", subtasks=True, 
           statuses=["todo", "in progress"])

This example will return all tasks and subtasks that are marked as "Todo" and "In Progress". These values can be changed depending on the statuses you have available in your list.

You can extend the calls above by passing any of the arguments to the ``get_tasks`` method. You can use as many or as few as you would like.



Working With Tasks
---------------
Now that you have a list of ``Task`` objects you can access the attributes of each task in a number of ways:

Example: Loop::

   c = client.ClickUpClient("YOUR_API_KEY")
   tasks = c.get_tasks(list_id)

   for task in tasks:
      print(task.name)


Example: Direct Access via an Index::

   c = client.ClickUpClient("YOUR_API_KEY")
   tasks = c.get_tasks(list_id)

   print(tasks[0].name])


Getting Tasks Associated with a List Object
---------------
Certain calls can be made directly from a parent object. We can access a single ``Task`` or all ``Tasks`` associated with a ``List`` with the following
methods. 

.. note:: IMPORTANT - When calling a method from a parent object you must pass in a reference to the ClickUpClient object as the first argument.

Example: Lookup Tasks via a List Object::

   c = client.ClickUpClient("YOUR_API_KEY")
   list = c.get_list(list_id)
   tasks = list.get_tasks(c)
   filtered_tasks = list.get_tasks(c, subtasks=True, statuses=["todo", "in progress"])
   task = list.get_task(c, task_id)
|
|

.. raw:: html

   <hr>

Task Methods
---------------

get_tasks()
++++++++++++
.. automethod:: clickupy.client.ClickUpClient.get_tasks
|
|

.. raw:: html

   <hr>
get_task()
++++++++++++
.. automethod:: clickupy.client.ClickUpClient.get_task
|

.. raw:: html

   <hr>
create_task()
++++++++++++
.. automethod:: clickupy.client.ClickUpClient.create_task
|
|
.. raw:: html

   <hr>
update_task()
++++++++++++
.. automethod:: clickupy.client.ClickUpClient.update_task
|
|
.. raw:: html

   <hr>

delete_task()
++++++++++++
.. automethod:: clickupy.client.ClickUpClient.delete_task
|
|
.. raw:: html

   <hr>

get_task_comments()
++++++++++++
.. automethod:: clickupy.client.ClickUpClient.get_task_comments
|
|
.. raw:: html

   <hr>


Lists
*****
.. autoclass:: clickupy.models.SingleList
    :members:
    :undoc-members:
    :show-inheritance:
|
|
.. raw:: html

   <hr>

List Methods
---------------

get_list()
++++++++++++
.. automethod:: clickupy.client.ClickUpClient.get_list
|
|
.. raw:: html

   <hr>
get_lists()
++++++++++++
.. automethod:: clickupy.client.ClickUpClient.get_lists
|
|
.. raw:: html

   <hr>
create_list()
++++++++++++
.. automethod:: clickupy.client.ClickUpClient.create_list
|
|
.. raw:: html

   <hr>
