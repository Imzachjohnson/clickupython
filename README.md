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

from clickupy import ClickupClient

API_KEY = 'YOUR API KEY'

client = ClickupClient(API_KEY)

# Example request
folders = client.get_folders(folder_id)
for folder in folders:
    print(folder.name)

```



## ClickupClient Functions

### Account


### List
* `get_list((list_id)`
* `get_lists(folder_id)`
* `create_list(folder_id, name, content, due_date, priority, status)`

### Folder
* `get_folder(folder_id)`
* `get_folders(space_id)`
* `create_folder(space_id, name)`
* `update_folder(folder_id: str, name: str)`
* `delete_folder(folder_id)`