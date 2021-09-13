<a href='https://clickupy.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/clickupy/badge/?version=latest' alt='Documentation Status' />
</a>

# clickupy

A client for working with the ClickUp API V2. It can be used to interact with the ClickUp API in your projects.

There are two ways to authenticate with ClickUp API 2.0, with a personal token or creating an application and authenticating with an OAuth2 flow. 

IMPORTANT - If you are creating an application for other's to use, it is highly recommended that you use the OAuth2 flow.

## Instructions
### 1) Installing
```pip install clickupy```

### 2) Library Usage
Using clickupy in your application takes just a couple quick steps.

To use the client for a personal account context (no actions on behalf of another user)

```python

from clickupy import ClickUpClient

API_KEY = 'YOUR API KEY'

client = ClickUpClient(API_KEY)

# Example request
c = client.ClickUpClient(API_KEY)
t = c.create_task("132216026", name="Test task", due_date="march 2 2021")

print(t.name)

```



## Current ClickUpClient Functions

### Task
* `get_task(task_id)`
* `get_tasks(list_id)`
* `create_task(list_id, name, description, priority, assignees, tags, status, due_date, start_date, notify_all)`
* `update_task(task_id, name, description, status, priority, time_estimate, archived, add_assignees,remove_assignees)`


### List
* `get_list(list_id)`
* `get_lists(folder_id)`
* `create_list(folder_id, name, content, due_date, priority, status)`

### Folder
* `get_folder(folder_id)`
* `get_folders(space_id)`
* `create_folder(space_id, name)`
* `update_folder(folder_id, name)`
* `delete_folder(folder_id)`

### Attachments
`upload_attachment(task_id, file_path)`

### Comments
* `get_task_comments(task_id)`
* `get_list_comments(list_id)`
* `get_chat_comments(view_id)`
* `update_comment(comment_id)`
* `delete_comment(comment_id)`
* `create_task_comment(task_id)`