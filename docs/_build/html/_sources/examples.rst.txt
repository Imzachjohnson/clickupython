Examples
====================================
Clickupy is a Python client for the ClickUp API and can be used to interact with the ClickUp API in your projects. Below are some examples to get you started with clickupy.


Tasks
*****

Creating a Task
---------------
Here's how to create a new ClickupClient instance and validate a personal API key with the ClickUp API and create a new task with a 
due date. When creating a new task, the only required arguments are list_id and name. Name will be the title of your list on ClickUp.

Example::

   c = client.ClickUpClient("YOUR_API_KEY")
   t = c.create_task("LIST_ID", name="Test Task", due_date="march 2 2021")


Each ``Task`` object has the following attributes:

``id``
``custom_id``
``name``
``text_content``
``description``
``status``
``orderindex``
``date_created``
``date_updated``
``date_closed``
``creator``
``task_assignees``
``task_checklists``
``task_tags``
``parent``
``priority``
``due_date``
``start_date``
``time_estimate``
``time_spent``
``custom_fields``
``list``
``folder``
``space``
``url``


Fetching all Tasks from a List
---------------
You can quickly get all tasks for a given list via the list id:

Example::

   c = client.ClickUpClient("YOUR_API_KEY")
   tasks = c.get_tasks("list_id")


Filtering Tasks
---------------
You can extend the call above by passing any of the following arguments to the ``get_tasks`` method. You can use as many or as few as you would like:

``archived (bool, optional): Include archived tasks in the retrieved tasks. Defaults to False.``
``page (int, optional): Page to fetch. Defaults to 0.``
``order_by (str, optional): Order by field, defaults to "created". Options: id, created, updated, due_date.``
``reverse (bool, optional): Reverse the order of the returned tasks. Defaults to False.``
``subtasks (bool, optional): Include archived tasks in the retrieved tasks. Defaults to False.``
``statuses (List[str], optional): Only retrieve tasks with the supplied status. Defaults to None.``
``include_closed (bool, optional): Include closed tasks in the query. Defaults to False.``
``assignees (List[str], optional): Retrieve tasks for specific assignees only. Defaults to None.``
``due_date_gt (str, optional): Retrieve tasks with a due date greater than the supplied date. Defaults to None.``
``due_date_lt (str, optional): Retrieve tasks with a due date less than the supplied date. Defaults to None.``
``date_created_gt (str, optional): Retrieve tasks with a creation date greater than the supplied date. Defaults to None.``
``date_created_lt (str, optional): Retrieve tasks with a creation date less than the supplied date. Defaults to None.``
``date_updated_gt (str, optional): Retrieve tasks where the last update date is greater than the supplied date. Defaults to None.``
``date_updated_lt (str, optional): Retrieve tasks where the last update date is greater than the supplied date. Defaults to None.``

Example::

   c = client.ClickUpClient("YOUR_API_KEY")
   tasks = c.get_tasks("list_id", date_updated_gt="august 1 2021", assignees=["4523","4562","5871"], include_closed=True)

This example will return all tasks that have been updated after August 1st, 2021 and are assigned to users with the ids of 4523, 4562, and 5871.
This request will also include tasks that have been marked as "closed."

Example::

   c = client.ClickUpClient("YOUR_API_KEY")
   tasks = c.get_tasks("list_id", subtasks=True, statuses=["todo", "in progress"])

This example will return all tasks and subtasks that are marked as "Todo" and "In Progress". These values can be changed depending on the statuses you have available in your list.

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

Getting a single Task
---------------
Example: Lookup via ClickUpClient::

   c = client.ClickUpClient("YOUR_API_KEY")
   task = c.get_task(task_id)

   print(task.name)


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