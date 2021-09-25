[![Documentation Status](https://readthedocs.org/projects/clickupy/badge/?version=latest)](https://clickupy.readthedocs.io/en/latest/?badge=latest)
[![CodeFactor](https://www.codefactor.io/repository/github/imzachjohnson/clickupy/badge)](https://www.codefactor.io/repository/github/imzachjohnson/clickupy)

# clickupy

A client for working with the ClickUp API V2. It can be used to interact with the ClickUp API in your projects.

There are two ways to authenticate with ClickUp API 2.0, with a personal token or creating an application and authenticating with an OAuth2 flow.

IMPORTANT - If you are creating an application for other's to use, it is highly recommended that you use the OAuth2 flow.

Documentation: Full documentation and examples can be found here: [clickupy documentation](https://clickupy.readthedocs.io/en/latest/)

## Instructions

### 1) Installing

`pip install clickupy`

### 2) Library Usage

Using clickupy in your application takes just a couple quick steps.

To use the client for a personal account context (no actions on behalf of another user)

```python

from clickupy import ClickUpClient

API_KEY = 'YOUR API KEY'

client = ClickUpClient(API_KEY)

# Example request
c = client.ClickUpClient(API_KEY)
t = c.create_task("task_id", name="Test task", due_date="march 2 2021")

print(t.name)

```

_For more examples, please refer to the [Documentation](https://clickupy.readthedocs.io/en/latest/)_

## Current ClickUpClient Functions

### Task

- `get_task(task_id)`
- `get_tasks(list_id, archived, page, order_by, reverse, subtasks, statuses, include_closed, assignees, due_date_gt, due_date_lt, date_created_gt, date_created_lt, date_updated_gt, date_updated_lt)`
- `create_task(list_id, name, description, priority, assignees, tags, status, due_date, start_date, notify_all)`
- `update_task(task_id, name, description, status, priority, time_estimate, archived, add_assignees,remove_assignees)`

### List

- `get_list(list_id)`
- `get_lists(folder_id)`
- `create_list(folder_id, name, content, due_date, priority, status)`
- `create_folderless_list(space_id, name, content, due_date, priority, assignee, status)`
- `update_list(list_id, name, content, due_date, due_date_time, priority, assignee, unset_status)`
- `delete_list(list_id)`
- `add_task_to_list(task_id, list_id)`
- `remove_task_from_list(task_id, list_id)`

### Folder

- `get_folder(folder_id)`
- `get_folders(space_id)`
- `create_folder(space_id, name)`
- `update_folder(folder_id, name)`
- `delete_folder(folder_id)`

### Attachments

`upload_attachment(task_id, file_path)`

### Comments

- `get_task_comments(task_id)`
- `get_list_comments(list_id)`
- `get_chat_comments(view_id)`
- `update_comment(comment_id)`
- `delete_comment(comment_id)`
- `create_task_comment(task_id)`

### Teams

- `get_teams()`

### Checklists

- `create_checklist(task_id, name)`
- `create_checklist_item(checklist_id, name, assignee)`
- `delete_checklist_item(checklist_id, checklist_item_id)`
- `update_checklist_item(checklist_id, checklist_item_id, name, resolved, parent)`

### Goals

- `create_goal(team_id, name, due_date, description, multiple_owners, owners, color)`
- `update_goal(goal_id, name, due_date, description, rem_owners, add_owners, color)`
- `delete_goal(goal_id)`
- `get_goal(goal_id)`
- `get_goals(team_id, include_completed)`

### Members

- `get_task_members(task_id)`
- `get_list_members(list_id)`

### Tags

- `get_space_tags(space_id)`
- `create_space_tag(space_id, name)`
- `update_tag(space_id, name, new_name)`
- `tag_task(task_id, tag_name)`
- `untag_task(task_id, tag_name)`

### Spaces

- `create_space(team_id, name, features)`
- `delete_space(space_id)`
- `get_space(space_id)`
- `get_spaces( team_id, archived)`

### Time Tracking

- `get_time_entries_in_range(team_id, start_date, end_date, assignees)`
- `get_single_time_entry(team_id, timer_id)`
- `start_timer(team_id, timer_id)`
- `stop_timer(team_id)`

## Contact

Created by Zach Johnson & Robert Mullis

Email: imzachjohnson@gmail.com, phoenix.scooter@gmail.com

### Acknowledgements

- [timefhuman](https://github.com/alvinwan/timefhuman)
- [word2number](https://github.com/akshaynagpal/w2n)

## License

Distributed under the GNU General Public License v3.0. See `LICENSE` for more information.
