import requests
import urllib
import urllib.parse
from urllib.parse import urlparse
import os
import json
import ntpath
from typing import List, Optional


from clickupython.helpers.timefuncs import fuzzy_time_to_seconds, fuzzy_time_to_unix
from clickupython.helpers import formatting
from clickupython import models
from clickupython import exceptions


API_URL = "https://api.clickup.com/api/v2/"


class ClickUpClient:
    def __init__(
        self,
        accesstoken: str,
        api_url: str = API_URL,
        default_space: str = None,
        default_list: str = None,
        default_task: str = None,
    ):
        self.api_url = api_url
        self.accesstoken = accesstoken
        self.request_count = 0
        self.default_space = default_space
        self.default_list = default_list
        self.default_task = default_task

    # Generates headers for use in GET, POST, DELETE, PUT requests

    def __headers(self, file_upload: bool = False):
        """Internal method to generate headers for HTTP requests. Generates headers for use in GET, POST, DELETE and PUT requests.

        Returns:
            :dict: Returns headers for HTTP requests
        """

        return (
            {"Authorization": self.accesstoken}
            if file_upload
            else {
                "Authorization": self.accesstoken,
                "Content-Type": "application/json",
            }
        )

    def __get_request(self, model, *additionalpath) -> json:
        """Performs a Get request to the ClickUp API"""
        path = formatting.url_join(API_URL, model, *additionalpath)
        response = requests.get(path, headers=self.__headers())
        self.request_count += 1
        response_json = response.json()
        if response.status_code == 429:
            raise exceptions.ClickupClientError(
                "Rate limit exceeded", response.status_code
            )
        if response.status_code in [401, 400, 404]:
            raise exceptions.ClickupClientError(
                response_json["err"], response.status_code
            )
        if response.ok:
            return response_json

    # Performs a Post request to the ClickUp API
    def __post_request(
        self, model, data, upload_files=None, file_upload=False, *additionalpath
    ):

        path = formatting.url_join(API_URL, model, *additionalpath)
        if data:
            if upload_files:
                response = requests.post(
                    path, headers=self.__headers(True), data=data, files=upload_files
                )
                self.request_count += 1
            else:
                response = requests.post(path, headers=self.__headers(), data=data)

                self.request_count += 1
            response_json = response.json()

            if response.status_code in [401, 400, 500, 404]:
                raise exceptions.ClickupClientError(
                    response_json["err"], response.status_code
                )
            if response.ok:
                return response_json
        else:
            response = requests.post(path, headers=self.__headers())
            response_json = response.json()
            if response.status_code in [401, 400, 500, 404]:
                raise exceptions.ClickupClientError(
                    response_json["err"], response.status_code
                )
            if response.ok:
                return response_json

    # Performs a Put request to the ClickUp API
    def __put_request(self, model, data, *additionalpath):
        path = formatting.url_join(API_URL, model, *additionalpath)
        response = requests.put(path, headers=self.__headers(), data=data)
        self.request_count += 1
        response_json = response.json()
        if response.status_code in [401, 400]:
            raise exceptions.ClickupClientError(
                response_json["err"], response.status_code
            )
        if response.ok:
            return response_json

    # Performs a Delete request to the ClickUp API
    def __delete_request(self, model, *additionalpath):
        path = formatting.url_join(API_URL, model, *additionalpath)
        response = requests.delete(path, headers=self.__headers())
        self.request_count += 1
        try:
            response_json = response.json()
        except:
            raise exceptions.ClickupClientError(
                "Invalid Json response", response.status_code
            )
        if response.ok:
            return response.status_code
        else:
            raise exceptions.ClickupClientError(
                response_json["err"], response.status_code
            )

    # Lists
    def get_list(self, list_id: str) -> models.SingleList:
        """Fetches a single list item from a given list id and returns a List object.

        Args:
            :list_id (str): The id of the ClickUp list.

        Returns:
            :models.SingleList: Returns an object of type List.
        """
        model = "list/"
        fetched_list = self.__get_request(model, list_id)

        return models.SingleList.build_list(fetched_list)

    def get_lists(self, folder_id: str) -> models.AllLists:
        """Fetches all lists from a given folder id and returns a list of List objects.

        Args:
            :folder_id (str): The ID of the ClickUp folder to be returned.

        Returns:
            :list.AllLists: Returns a list of type AllLists.
        """
        model = "folder/"
        fetched_lists = self.__get_request(model, folder_id)
        return models.AllLists.build_lists(fetched_lists)

    def create_list(
        self,
        folder_id: str,
        name: str,
        content: str,
        due_date: str,
        priority: int,
        status: str,
    ) -> models.SingleList:
        """Creates and returns a List object in a folder from a given folder ID.

        Args:
            :folder_id (str): The ID of the ClickUp folder.
            :name (str): The name of the created list.
            :content (str): The description content of the created list.
            :due_date (str): The due date of the created list.
            :priority (int): An integer 1 : Urgent, 2 : High, 3 : Normal, 4 : Low.
            :status (str): Refers to the List color rather than the task Statuses available in the List.

        Returns:
            :list.SingleList: Returns an object of type SingleList.
        """
        data = {
            "name": name,
            "content": content,
            "due_date": due_date,
            "status": status,
        }
        model = "folder/"
        created_list = self.__post_request(
            model, json.dumps(data), None, False, folder_id, "list"
        )
        if created_list:
            return models.SingleList.build_list(created_list)

    def create_folderless_list(
        self,
        space_id: str,
        name: str,
        content: str = None,
        due_date: str = None,
        priority: int = None,
        assignee: str = None,
        status: str = None,
    ) -> models.SingleList:

        arguments = {}
        arguments.update(vars())
        arguments.pop("self", None)
        arguments.pop("arguments", None)
        arguments.pop("space_id", None)

        final_dict = json.dumps({k: v for k, v in arguments.items() if v is not None})

        model = "space/"
        created_list = self.__post_request(
            model, final_dict, None, False, space_id, "list"
        )
        if created_list:
            return models.SingleList.build_list(created_list)

    # //TODO Add unit tests
    def update_list(
        self,
        list_id: str,
        name: str = None,
        content: str = None,
        due_date: str = None,
        due_date_time: bool = None,
        priority: int = None,
        assignee: str = None,
        unset_status: bool = None,
    ) -> models.SingleList:

        if priority and priority not in range(1, 4):
            raise exceptions.ClickupClientError(
                "Priority must be in range of 0-4.", "Priority out of range"
            )

        if due_date:
            due_date = fuzzy_time_to_unix(due_date)

        arguments = {}
        arguments.update(vars())
        arguments.pop("self", None)
        arguments.pop("arguments", None)
        arguments.pop("list_id", None)

        final_dict = json.dumps({k: v for k, v in arguments.items() if v is not None})
        print(final_dict)
        model = "list/"
        updated_list = self.__put_request(model, final_dict, list_id)
        if updated_list:
            return models.SingleList.build_list(updated_list)

    def delete_list(self, list_id: str) -> bool:

        """Deletes a list via a given list id.

        Returns:
            bool: Returns True if the list was successfully deleted.
        """
        model = "list/"
        self.__delete_request(model, list_id)
        return True

    def add_task_to_list(
        self,
        task_id: str,
        list_id: str,
    ) -> models.Task:
        """Adds a task to a list via a gen task id and list id.

        Args:
            task_id (str): The id of the task to be added to a list.
            list_id (str): The id of the list to add the task to.

        Returns:
            models.Task: Returns an object of type Task.
        """
        model = "list/"
        task = self.__post_request(model, None, None, False, list_id, "task", task_id)

        return True

    def remove_task_from_list(
        self,
        task_id: str,
        list_id: str,
    ) -> bool:
        """Removes a task from a list via a given task id and list id.

        Args:
            :task_id (str): The id of the task to remove.
            :list_id (str): The id of the list to remove the task from.

        Returns:
           :bool: Returns True.
        """
        model = "list/"
        task = self.__delete_request(model, list_id, "task", task_id)
        return True

    # Folders

    def get_folder(self, folder_id: str) -> models.Folder:
        """Fetches a single folder item from a given folder id and returns a Folder object.

        Args:
            :folder_id (str): The ID of the ClickUp folder to retrieve.

        Returns:
            :Folder: Returns an object of type Folder.
        """
        model = "folder/"
        fetched_folder = self.__get_request(model, folder_id)
        if fetched_folder:
            return models.Folder.build_folder(fetched_folder)

    def get_folders(self, space_id: str) -> models.Folders:
        """Fetches all folders from a given space ID and returns a list of Folder objects.

        Args:
            :space_id (str): The ID of the ClickUp space to retrieve the list of folder from.

        Returns:
            :Folders: Returns a list of Folder objects.
        """
        model = "space/"
        fetched_folders = self.__get_request(model, space_id, "folder")
        if fetched_folders:
            return models.Folders.build_folders(fetched_folders)

    def create_folder(self, space_id: str, name: str) -> models.Folder:
        """Creates and returns a Folder object in a space from a given space ID.

        Args:
            :space_id (str): The ID of the ClickUp space to create the folder inside.
            :name (str): String value that the created folder will utilize as its name.

        Returns:
            :Folder: Returns the created Folder object.
        """
        data = {
            "name": name,
        }
        model = "space/"
        created_folder = self.__post_request(
            model, json.dumps(data), None, False, space_id, "folder"
        )
        if created_folder:
            return models.Folder.build_folder(created_folder)

    def update_folder(self, folder_id: str, name: str) -> models.Folder:
        """Updates the name of a folder given the folder ID.

        Args:
            :folder_id (str): The ID of the ClickUp folder to update.
            :name (str): String that the folder name will be updated to reflect.

        Returns:
            :Folder: Returns the updated Folder as an object.
        """
        data = {
            "name": name,
        }
        model = "folder/"
        updated_folder = self.__put_request(model, json.dumps(data), folder_id)
        if updated_folder:
            return models.Folder.build_folder(updated_folder)

    def delete_folder(self, folder_id: str) -> None:
        """Deletes a folder from a given folder ID.

        Args:
            :folder_id (str): The ID of the ClickUp folder to delete.
        """
        model = "folder/"
        deleted_folder_status = self.__delete_request(model, folder_id)
        return True

    # Tasks
    def upload_attachment(self, task_id: str, file_path: str) -> models.Attachment:
        """Uploads an attachment to a ClickUp task.

        Args:
            :task_id (str): The ID of the task to upload to.
            :file_path (str): The filepath of the file to upload.

        Returns:
            :Attachment: Returns an attachment object.
        """

        if os.path.exists(file_path):

            with open(file_path, "rb") as f:
                files = [("attachment", (f.name, open(file_path, "rb")))]
                data = {"filename": ntpath.basename(f.name)}
                model = "task/" + task_id
                uploaded_attachment = self.__post_request(
                    model, data, files, True, "attachment"
                )

                if uploaded_attachment:
                    final_attachment = models.Attachment.build_attachment(
                        uploaded_attachment
                    )
                return final_attachment

    # // TODO Add "Include subtasks option"
    def get_task(self, task_id: str) -> models.Task:
        """Fetches a single ClickUp task item and returns a Task object.

        Args:
            :task_id (str): The ID of the task to return.

        Returns:
            :Task: Returns an object of type Task.
        """
        model = "task/"
        fetched_task = self.__get_request(model, task_id)
        final_task = models.Task.build_task(fetched_task)
        if final_task:
            return final_task

    def get_team_tasks(
        self,
        team_Id: str,
        page: int = 0,
        order_by: str = "created",
        reverse: bool = False,
        subtasks: bool = False,
        space_ids: List[str] = None,
        project_ids: List[str] = None,
        list_ids: List[str] = None,
        statuses: List[str] = None,
        include_closed: bool = False,
        assignees: List[str] = None,
        tags: List[str] = None,
        due_date_gt: str = None,
        due_date_lt: str = None,
        date_created_gt: str = None,
        date_created_lt: str = None,
        date_updated_gt: str = None,
        date_updated_lt: str = None,
    ) -> models.Tasks:
        """Gets filtered tasks for a team.

        Args:
            :team_Id (str): The id of the team to get tasks for.
            :page (int, optional): The starting page number. Defaults to 0.
            :order_by (str, optional):  Order by field, defaults to "created". Options: id, created, updated, due_date.
            :reverse (bool, optional): [description]. Defaults to False.
            :subtasks (bool, optional): [description]. Defaults to False.
            :space_ids (List[str], optional): [description]. Defaults to None.
            :project_ids (List[str], optional): [description]. Defaults to None.
            :list_ids (List[str], optional): [description]. Defaults to None.
            :statuses (List[str], optional): [description]. Defaults to None.
            :include_closed (bool, optional): [description]. Defaults to False.
            :assignees (List[str], optional): [description]. Defaults to None.
            :tags (List[str], optional): [description]. Defaults to None.
            :due_date_gt (str, optional): [description]. Defaults to None.
            :due_date_lt (str, optional): [description]. Defaults to None.
            :date_created_gt (str, optional): [description]. Defaults to None.
            :date_created_lt (str, optional): [description]. Defaults to None.
            :date_updated_gt (str, optional): [description]. Defaults to None.
            :date_updated_lt (str, optional): [description]. Defaults to None.

        Raises:
            exceptions.ClickupClientError: [description]

        Returns:
            models.Tasks: [description]
        """
        if order_by not in ["id", "created", "updated", "due_date"]:
            raise exceptions.ClickupClientError(
                "Options are: id, created, updated, due_date", "Invalid order_by value"
            )

        supplied_values = [
            f"page={page}",
            f"order_by={order_by}",
            f"reverse={str(reverse).lower()}",
        ]

        if statuses:
            supplied_values.append(
                f"{urllib.parse.quote_plus('statuses[]')}={','.join(statuses)}"
            )
        if assignees:
            supplied_values.append(
                f"{urllib.parse.quote_plus('assignees[]')}={','.join(assignees)}"
            )
        if due_date_gt:
            supplied_values.append(f"due_date_gt={fuzzy_time_to_unix(due_date_gt)}")
        if due_date_lt:
            supplied_values.append(f"due_date_lt={fuzzy_time_to_unix(due_date_lt)}")
        if space_ids:
            supplied_values.append(
                f"{urllib.parse.quote_plus('space_ids[]')}={','.join(space_ids)}"
            )
        if project_ids:
            supplied_values.append(
                f"{urllib.parse.quote_plus('project_ids[]')}={','.join(project_ids)}"
            )
        if list_ids:
            supplied_values.append(
                f"{urllib.parse.quote_plus('list_ids[]')}={','.join(list_ids)}"
            )
        if date_created_gt:
            supplied_values.append(f"date_created_gt={date_created_gt}")
        if date_created_lt:
            supplied_values.append(f"date_created_lt={date_created_lt}")
        if date_updated_gt:
            supplied_values.append(f"date_updated_gt={date_updated_gt}")
        if date_updated_lt:
            supplied_values.append(f"date_updated_lt={date_updated_lt}")
        if subtasks:
            supplied_values.append(f"subtasks=true")

        joined_url = f"task?{'&'.join(supplied_values)}"

        model = "team/"
        fetched_tasks = self.__get_request(model, team_Id, joined_url)
        if fetched_tasks:
            return models.Tasks.build_tasks(fetched_tasks)

    def get_tasks(
        self,
        list_id: str,
        archived: bool = False,
        page: int = 0,
        order_by: str = "created",
        reverse: bool = False,
        subtasks: bool = False,
        statuses: List[str] = None,
        include_closed: bool = False,
        assignees: List[str] = None,
        due_date_gt: str = None,
        due_date_lt: str = None,
        date_created_gt: str = None,
        date_created_lt: str = None,
        date_updated_gt: str = None,
        date_updated_lt: str = None,
    ) -> models.Tasks:

        """The maximum number of tasks returned in this response is 100. When you are paging this request, you should check list limit
        against the length of each response to determine if you are on the last page.

        Args:
            :list_id (str):
                The ID of the list to retrieve tasks from.
            :archived (bool, optional):
                Include archived tasks in the retrieved tasks. Defaults to False.
            :page (int, optional):
                Page to fetch (starts at 0). Defaults to 0.
            :order_by (str, optional):
                Order by field, defaults to "created". Options: id, created, updated, due_date.
            :reverse (bool, optional):
                Reverse the order of the returned tasks. Defaults to False.
            :subtasks (bool, optional):
                Include archived tasks in the retrieved tasks. Defaults to False.
            :statuses (List[str], optional):
                Only retrieve tasks with the supplied status. Defaults to None.
            :include_closed (bool, optional):
                Include closed tasks in the query. Defaults to False.
            :assignees (List[str], optional):
                Retrieve tasks for specific assignees only. Defaults to None.
            :due_date_gt (str, optional):
                Retrieve tasks with a due date greater than the supplied date. Defaults to None.
            :due_date_lt (str, optional): Retrieve tasks with a due date less than the supplied date. Defaults to None.
            :date_created_gt (str, optional):
                Retrieve tasks with a creation date greater than the supplied date. Defaults to None.
            :date_created_lt (str, optional):
                Retrieve tasks with a creation date less than the supplied date. Defaults to None.
            :date_updated_gt (str, optional):
                Retrieve tasks where the last update date is greater than the supplied date. Defaults to None.
            :date_updated_lt (str, optional): Retrieve tasks where the last update date is greater than the supplied date. Defaults to None.

        Raises:
            :exceptions.ClickupClientError: Invalid order_by value

        Returns:
            :models.Tasks: Returns a list of item Task.
        """

        if order_by not in ["id", "created", "updated", "due_date"]:
            raise exceptions.ClickupClientError(
                "Options are: id, created, updated, due_date", "Invalid order_by value"
            )

        supplied_values = [
            f"archived={str(archived).lower()}",
            f"page={page}",
            f"order_by={order_by}",
            f"reverse={str(reverse).lower()}",
            f"include_closed={str(include_closed).lower()}",
        ]

        if statuses:
            supplied_values.append(
                f"{urllib.parse.quote_plus('statuses[]')}={','.join(statuses)}"
            )
        if assignees:
            supplied_values.append(
                f"{urllib.parse.quote_plus('assignees[]')}={','.join(assignees)}"
            )
        if due_date_gt:
            supplied_values.append(f"due_date_gt={fuzzy_time_to_unix(due_date_gt)}")
        if due_date_lt:
            supplied_values.append(f"due_date_lt={fuzzy_time_to_unix(due_date_lt)}")
        if date_created_gt:
            supplied_values.append(f"date_created_gt={date_created_gt}")
        if date_created_lt:
            supplied_values.append(f"date_created_lt={date_created_lt}")
        if date_updated_gt:
            supplied_values.append(f"date_updated_gt={date_updated_gt}")
        if date_updated_lt:
            supplied_values.append(f"date_updated_lt={date_updated_lt}")
        if subtasks:
            supplied_values.append(f"subtasks=true")

        joined_url = f"task?{'&'.join(supplied_values)}"

        model = "list/"
        fetched_tasks = self.__get_request(model, list_id, joined_url)
        if fetched_tasks:
            return models.Tasks.build_tasks(fetched_tasks)

    def create_task(
        self,
        list_id: str,
        name: str,
        description: str = None,
        priority: int = None,
        assignees: [] = None,
        tags: [] = None,
        status: str = None,
        due_date: str = None,
        start_date: str = None,
        notify_all: bool = True,
    ) -> models.Task:

        """[summary]

        Args:
            :list_id (str): [description]
            :name (str): [description]
            :description (str, optional): [description]. Defaults to None.
            :priority (int, optional): [description]. Defaults to None.
            :assignees ([type], optional): [description]. Defaults to None.
            :tags ([type], optional): [description]. Defaults to None.
            :status (str, optional): [description]. Defaults to None.
            :due_date (str, optional): [description]. Defaults to None.
            :start_date (str, optional): [description]. Defaults to None.
            :notify_all (bool, optional): [description]. Defaults to True.

        Raises:
            :exceptions.ClickupClientError: [description]

        Returns:
            :models.Task: [description]
        """
        if priority and priority not in range(1, 4):
            raise exceptions.ClickupClientError(
                "Priority must be in range of 0-4.", "Priority out of range"
            )
        if due_date:
            due_date = fuzzy_time_to_unix(due_date)

        arguments = {}
        arguments.update(vars())
        arguments.pop("self", None)
        arguments.pop("arguments", None)
        arguments.pop("list_id", None)

        final_dict = json.dumps({k: v for k, v in arguments.items() if v is not None})

        model = "list/"
        created_task = self.__post_request(
            model, final_dict, None, False, list_id, "task"
        )

        if created_task:
            return models.Task.build_task(created_task)

    def update_task(
        self,
        task_id,
        name: str = None,
        description: str = None,
        status: str = None,
        priority: int = None,
        time_estimate: int = None,
        archived: bool = None,
        add_assignees: List[str] = None,
        remove_assignees: List[int] = None,
    ) -> models.Task:

        """[summary]

        Args:
            :task_id ([type]): The ID of the ClickUp task to update.
            :name (str, optional): Sting value to update the task name to. Defaults to None.
            :description (str, optional): Sting value to update the task description to. Defaults to None.
            :status (str, optional): String value of the tasks status. Defaults to None.
            :priority (int, optional): Priority of the task. Range 1-4. Defaults to None.
            :time_estimate (int, optional): Time estimate of the task. Defaults to None.
            :archived (bool, optional): Whether the task should be archived or not. Defaults to None.
            :add_assignees (List[str], optional): List of assignee IDs to add to the task. Defaults to None.
            :remove_assignees (List[int], optional): List of assignee IDs to remove from the task. Defaults to None.

        Raises:
            :exceptions.ClickupClientError: Raises "Priority out of range" exception for invalid priority range.

        Returns:
            :models.Task: Returns an object of type Task.
        """
        if priority and priority not in range(1, 4):
            raise exceptions.ClickupClientError(
                "Priority must be in range of 0-4.", "Priority out of range"
            )

        arguments = {}
        arguments.update(vars())
        arguments.pop("self", None)
        arguments.pop("arguments", None)
        arguments.pop("task_id", None)
        arguments.pop("add_assignees", None)
        arguments.pop("remove_assignees", None)

        if add_assignees and remove_assignees:
            arguments.update(
                {"assignees": {"add": add_assignees, "rem": remove_assignees}}
            )
        elif add_assignees:
            arguments.update({"assignees": {"add": add_assignees}})
        elif remove_assignees:
            arguments.update({"assignees": {"rem": remove_assignees}})

        final_dict = json.dumps({k: v for k, v in arguments.items() if v is not None})

        model = "task/"
        updated_task = self.__put_request(model, final_dict, task_id)
        if updated_task:
            return models.Task.build_task(updated_task)

    def delete_task(self, task_id: str) -> None:
        """Deletes a task via a given task ID.

        Args:
            :folder_id (str): The ID of the ClickUp task to delete.
        """
        model = "task/"
        deleted_task_status = self.__delete_request(model, task_id)
        return True

    # Comments
    def get_task_comments(self, task_id: str) -> models.Comments:
        """Get all the comments for a task from a given task id.

        Args:
            :task_id (str): The id of the ClickUp task to retrieve comments from.

        Returns:
            :models.Comments: Returns an object of type Comments.
        """
        model = "task/"
        fetched_comments = self.__get_request(model, task_id, "comment")
        final_comments = models.Comments.build_comments(fetched_comments)
        if final_comments:
            return final_comments

    def get_list_comments(self, list_id: str) -> models.Comments:
        """Get all the comments for a list from a given list id.

        Args:
            :list_id (str): The id of the ClickUp list to retrieve comments from.

        Returns:
            :models.Comments: Returns an object of type Comments.
        """
        model = "list/"
        fetched_comments = self.__get_request(model, list_id, "comment/")
        final_comments = models.Comments.build_comments(fetched_comments)
        if final_comments:
            return final_comments

    def get_chat_comments(self, view_id: str) -> models.Comments:
        """Get all the comments for a chat from a given view id.

        Args:
            :view_id (str): The id of the view to retrieve comments from.

        Returns:
            :models.Comments: Returns an object of type Comments.
        """
        model = "view/"
        fetched_comments = self.__get_request(model, view_id, "comment/")
        print(fetched_comments)
        final_comments = models.Comments.build_comments(fetched_comments)
        if final_comments:
            return final_comments

    def update_comment(
        self,
        comment_id: str,
        comment_text: str = None,
        assignee: str = None,
        resolved: bool = None,
    ) -> models.Comment:
        """Update a ClickUp comment's content, assignee and resolution status.

        Args:
            :comment_id (str): The id of the comment to update
            :comment_text (str, optional): The new content of the comment. Defaults to None.
            :assignee (str, optional): The id of an assignee. Defaults to None.
            :resolved (bool, optional): Comment resolution status. Defaults to None.

        Returns:
            :models.Comment: [description]
        """
        arguments = {}
        arguments.update(vars())
        arguments.pop("self", None)
        arguments.pop("arguments", None)
        arguments.pop("comment_id", None)

        model = "comment/"

        final_dict = json.dumps({k: v for k, v in arguments.items() if v is not None})

        updated_comment = self.__put_request(model, final_dict, comment_id)

        return True

    def delete_comment(self, comment_id: str) -> bool:
        """Deletes a comment via a given comment id.

        Args:
            :comment_id (str): The id of the comment to delete.

        Returns:
            :bool: True if successful.
        """
        model = "comment/"
        deleted_comment_status = self.__delete_request(model, comment_id)
        return True

    def create_task_comment(
        self,
        task_id: str,
        comment_text: str,
        assignee: str = None,
        notify_all: bool = True,
    ) -> models.Comment:
        """Create a comment on a task via a given task id.

        Args:
            :task_id (str): The id of the task to comment on.
            :comment_text (str): The text of the comment.
            :assignee (str, optional): The id of a user to add as an assignee. Defaults to None.
            :notify_all (bool, optional): Notify all valid users of the comment's creation. Defaults to True.

        Returns:
            :models.Comment: Returns an object of type Comment.
        """
        arguments = {}
        arguments.update(vars())
        arguments.pop("self", None)
        arguments.pop("arguments", None)
        arguments.pop("task_id", None)

        model = "task/"

        final_dict = json.dumps({k: v for k, v in arguments.items() if v is not None})

        created_comment = self.__post_request(
            model, final_dict, None, False, task_id, "comment"
        )

        final_comment = models.Comment.build_comment(created_comment)
        if final_comment:
            return final_comment

    def create_chat_comment(
        self,
        view_id: str,
        comment_text: str,
        notify_all: bool = True,
    ) -> models.Comment:
        """Create a comment on a chat via a given chat view id.

        Args:
            :view_id (str): The id of the chat to comment on.
            :comment_text (str): The text of the comment.
            :notify_all (bool, optional): Notify all valid users of the comment's creation. Default to True.

        Returns:
            :models.Comment: Returns an object of type Comment.
        """
        arguments = {}
        arguments.update(vars())
        arguments.pop("self", None)
        arguments.pop("arguments", None)
        arguments.pop("view_id", None)

        model = "view/"

        final_dict = json.dumps({k: v for k, v in arguments.items() if v is not None})

        created_comment = self.__post_request(
            model, final_dict, None, False, view_id, "comment"
        )

        final_comment = models.Comment.build_comment(created_comment)
        if final_comment:
            return final_comment

    # Teams
    def get_teams(self) -> models.Teams:
        """Get all teams from a workspace. Teams is the legacy term for what are now called Workspaces in ClickUp. For compatibility,
        the term team is still used in this API. This is NOT the new "Teams" feature which represents a group of users.

        Returns:
             :models.Teams: Returns an object of type Teams.
        """
        model = "team"
        fetched_teams = self.__get_request(model)
        final_teams = models.Teams.build_teams(fetched_teams)
        if final_teams:
            return final_teams

    # Checklists
    def create_checklist(self, task_id: str, name: str) -> models.Checklist:
        """Create a checklist in a task via a given task id.

        Args:
            :task_id (str): The id of the task to create a checklist in.
            :name (str): The name for the new checklist.

        Returns:
            :models.Checklist: Returns and object of type Checklist.
        """
        data = {
            "name": name,
        }

        model = "task/"
        created_checklist = self.__post_request(
            model, json.dumps(data), None, False, task_id, "checklist"
        )
        return models.Checklists.build_checklist(created_checklist)

    def create_checklist_item(
        self, checklist_id: str, name: str, assignee: str = None
    ) -> models.Checklist:
        """create_checklist_item Creates an item in a ClickUp checklist via a given checklist id.

        Args:
            :checklist_id (str): The id of the checklist to create a new item in.
            :name (str): The name of the new checklist item.
            :assignee (str, optional): The user id to assign the checklist item to. Defaults to None.

        Returns:
            :models.Checklist: Returns and object of type Checklist.
        """
        data = {}

        data = {"name": name, "assignee": assignee} if assignee else {"name": name}
        model = "checklist/"
        created_checklist = self.__post_request(
            model, json.dumps(data), None, False, checklist_id, "checklist_item"
        )
        return models.Checklists.build_checklist(created_checklist)

    def update_checklist(
        self, checklist_id: str, name: str = None, postion: int = None
    ) -> models.Checklist:
        """update_checklist Updates a ClickUp checklist.

        Args:
            :checklist_id (str): The id of the checklist to be updated.
            :name (str, optional): The name to update the checklist to. Defaults to None.
            :postion (int, optional): The order position to update the checklist to. Defaults to None.

        Returns:
            :models.Checklist: Returns an object of type Checklist.
        """
        if not name and not postion:
            return

        data = {}

        if name:
            data.update({"name": name})
        if postion:
            data.update({"postition": position})

        model = "checklist/"
        updated_checklist = self.__put_request(model, json.dumps(data), checklist_id)
        if updated_checklist:
            return models.Checklists.build_checklist(updated_checklist)

    def delete_checklist(self, checklist_id: str) -> bool:
        """delete_checklist Delete a checklist via a given checklist id.

        Args:
            :checklist_id (str): The id of the ClickUp checklist to be deleted.

        Returns:
            :bool: Returns True
        """
        model = "checklist/"
        self.__delete_request(model, checklist_id)
        return True

    def delete_checklist_item(self, checklist_id: str, checklist_item_id: str) -> bool:
        """Deletes an item from a checklist via a given checklist id and item id.

        Args:
            :checklist_id (str): The id of the ClickUp checklist to delete an item from.
            :checklist_item_id (str): The id of the checklist item to be deleted.
        """
        model = "checklist/"
        self.__delete_request(model, checklist_id, "checklist_item", checklist_item_id)
        return True

    def update_checklist_item(
        self,
        checklist_id: str,
        checklist_item_id: str,
        name: str = None,
        resolved: bool = None,
        parent: str = None,
    ) -> models.Checklist:
        """Updates an item in a checklist via a given checklist id and item id.

        Args:
            :checklist_id (str): The id of the checklist the item resides in.
            :checklist_item_id (str): The id of the checklist item to be updated.
            :name (str, optional): New name for the checklist item. Defaults to None.
            :resolved (bool, optional): boolean value indicated the resolution status of the checklist item. Defaults to None.
            :parent (str, optional): The new parent for the checklist item. Defaults to None.

        Returns:
            :models.Checklist: [description]
        """
        arguments = {}
        arguments.update(vars())
        arguments.pop("self", None)
        arguments.pop("arguments", None)
        arguments.pop("checklist_id", None)
        arguments.pop("checklist_item_id", None)

        model = "checklist/"

        final_dict = json.dumps({k: v for k, v in arguments.items() if v is not None})

        item_update = self.__put_request(
            model, final_dict, checklist_id, "checklist_item", checklist_item_id
        )

        final_update = models.Checklists.build_checklist(item_update)
        if final_update:
            return final_update

    # Members

    def get_task_members(self, task_id: str) -> models.Members:
        """Get all members assigned to a specific task via a task id.

        Args:
            :task_id (str): The id of the task to get members of.

        Returns:
            :models.Members: Returns an object of type Members.
        """

        model = "task/"

        task_members = self.__get_request(model, task_id, "member")
        return models.Members.build_members(task_members)

    def get_list_members(self, list_id: str) -> models.Members:
        """Get all members assigned to a specific list via a list id.

        Args:
            :list_id (str): The id of the list to get members of.

        Returns:
            :models.Members: Returns an object of type Members.
        """
        model = "list/"

        task_members = self.__get_request(model, list_id, "member")
        return models.Members.build_members(task_members)

    # Goals

    def create_goal(
        self,
        team_id,
        name: str,
        due_date: str = None,
        description: str = None,
        multiple_owners: bool = True,
        owners: List[int] = None,
        color: str = None,
    ) -> models.Goal:
        """Create a new goal for a team given a team id.

        Args:
            :team_id ([type]): [description]
            :name (str, optional): The name of the goal.
            :due_date (str, optional): The due date of the goal. Defaults to None.
            :description (str, optional): The goal description. Defaults to None.
            :multiple_owners (bool, optional): Indicated whether the goal should have multiple owners. Defaults to True.
            :owners (List[int], optional): If multiple owners is True, a supplied list of user ids to assign as owners. Defaults to None.
            :color (str, optional): Hex value for color of the goal. Defaults to None.

        Returns:
            :models.Goal: Returns an object of type Goal.
        """
        arguments = {}
        arguments.update(vars())
        arguments.pop("self", None)
        arguments.pop("arguments", None)
        arguments.pop("team_id", None)
        arguments.pop("owners", None)

        if multiple_owners and owners:
            arguments.update({"owners": owners})

        final_dict = json.dumps({k: v for k, v in arguments.items() if v is not None})

        model = "team/"
        created_goal = self.__post_request(
            model, final_dict, None, False, team_id, "goal"
        )
        if created_goal:
            return models.Goals.build_goals(created_goal)

    def update_goal(
        self,
        goal_id: str,
        name: str = None,
        due_date: str = None,
        description: str = None,
        rem_owners: List[str] = None,
        add_owners: List[str] = None,
        color: str = None,
    ) -> models.Goal:
        """Updates a goal via a given goal id.

        Args:
            :goal_id (str): The id of the goal to be updated.
            :name (str, optional): New name for the goal. Defaults to None.
            :due_date (str, optional): Due date for goal. Defaults to None.
            :description (str, optional): Description of the goal. Defaults to None.
            :rem_owners (List[str], optional): Remove owners from the goal. Defaults to None.
            :add_owners (List[str], optional): Add owners to the goal. Defaults to None.
            :color (str, optional): The color for the goal. Defaults to None.

        Returns:
            models.Goal: [description]
        """
        arguments = {}
        arguments.update(vars())
        arguments.pop("self", None)
        arguments.pop("arguments", None)
        arguments.pop("goal_id", None)

        final_dict = json.dumps({k: v for k, v in arguments.items() if v is not None})

        model = "goal/"
        updated_goal = self.__put_request(model, final_dict, goal_id)
        if updated_goal:
            return models.Goals.build_goals(updated_goal)

    def delete_goal(self, goal_id: str) -> bool:
        """Delete a goal via a given goal id.

        Args:
            :goal_id (str): The id of the goal to delete.

        Returns:
            :bool: Returns True.
        """
        model = "goal/"
        self.__delete_request(model, goal_id)
        return True

    def get_goal(self, goal_id: str) -> models.Goal:
        """get_goal fetch a goal via a given goal id.
        Args:
            :goal_id (str): The id of the goal to be fetched.
        Returns:
            :models.Goal: Returns an object of type Goal.
        """
        model = "goal/"
        fetched_goal = self.__get_request(model, goal_id)
        final_goal = models.Goals.build_goals(fetched_goal)
        if final_goal:
            return final_goal

    def get_goals(self, team_id: str, include_completed: bool = False) -> models.Goals:
        """get_goals Returns a list of goals for a team via a given team id.
        Args:
            :team_id (str): The id of the team to fetch goals for.
            :include_completed (bool, optional): Setting this to true will include completed goals in the query. Defaults to False.

        Returns:
            :models.Goals: Returns an object of type Goals.
        """
        model = "team/"

        if include_completed:
            fetched_goals = self.__get_request(
                model, team_id, "goal?include_completed=true"
            )
        else:
            fetched_goals = self.__get_request(
                model, team_id, "goal?include_completed=false"
            )

        final_goals = models.GoalsList.build_goals(fetched_goals)
        if final_goals:
            return final_goals

    # Tags

    def get_space_tags(self, space_id: str) -> models.Tags:
        """Gets all tags from a ClickUp space given the space id.

        Args:
            :space_id (str): The id of the space to return tags from.

        Returns:
            :models.Tags: Returns an object of type Tags.
        """
        model = "space/"

        fetched_tags = self.__get_request(model, space_id, "tag")

        final_tags = models.Tags.build_tags(fetched_tags)

        if final_tags:
            return final_tags

    def create_space_tag(
        self,
        space_id,
        name: str,
    ) -> models.Tag:
        """Creates a tag to be utilized in a space.

        Args:
            :space_id ([type]): The id of the space to create a tag for.
            :name (str): the name of the created tag.

        Returns:
            :models.Tag: Returns an object of type Tag.
        """
        arguments = {}
        arguments.update(vars())
        arguments.pop("self", None)
        arguments.pop("arguments", None)
        arguments.pop("space_id", None)

        final_dict = {k: v for k, v in arguments.items() if v is not None}
        final_tag = json.dumps({"tag": final_dict})

        model = "space/"
        created_tag = self.__post_request(
            model, final_tag, None, False, space_id, "tag"
        )
        print(created_tag)

        return True

    # // TODO #34 Finalize update_tag function. API endpoint doesn't seem to do anything?

    # def update_tag(
    #     self,
    #     space_id: str,
    #     tag_name: str,
    #     new_name: str,
    # ):

    #     final_dict = {"tag_name": new_name}

    #     model = "space/"
    #     updated_tag = self.__put_request(model, None, space_id, "tag", tag_name)
    #     if updated_tag:
    #         return models.Tags.build_tags(updated_tag)
    #     return None

    def tag_task(
        self,
        task_id: str,
        tag_name: str,
    ):

        model = "task/"
        self.__post_request(model, None, None, False, task_id, "tag", tag_name)

        return True

    def untag_task(
        self,
        task_id: str,
        tag_name: str,
    ):
        model = "task/"
        self.__delete_request(model, task_id, "tag", tag_name)
        return True

    # Spaces

    def create_space(
        self, team_id: str, name: str, features: models.Features
    ) -> models.Space:
        """create_space Create's a new ClickUp space.

        Args:
            :team_id (str): Id of the team to create the space for.
            :name (str): The name of the created space.
            :features (models.Features): Features to enable or disable in the newly created space.

        Returns:
            :models.Space: Returns an object of type Space.
        """
        final_dict = json.dumps(
            {
                "name": name,
                "multiple_assignees": features.multiple_assignees,
                "features": features.all_features,
            }
        )

        model = "team/"
        created_space = self.__post_request(
            model, final_dict, None, False, team_id, "space"
        )
        print(created_space)
        if created_space:
            return models.Space.build_space(created_space)

    def delete_space(self, space_id: str):

        model = "space/"
        self.__delete_request(model, space_id)
        return True

    def get_space(self, space_id: str):

        model = "space/"

        fetched_space = self.__get_request(model, space_id)

        if fetched_space:
            return models.Space.build_space(fetched_space)

    def get_spaces(self, team_id: str, archived: bool = False):

        path = "space?archived=false"

        if archived:
            path = "space?archived=true"

        model = "team/"

        fetched_spaces = self.__get_request(model, team_id, path)

        if fetched_spaces:
            return models.Spaces.build_spaces(fetched_spaces)

    # Shared Hierarchy
    # Returns all resources you have access to where you don't have access to its parent.
    # For example, if you have a access to a shared task, but don't have access to its parent list, it will come back in this request.

    def get_shared_hierarchy(self, team_id: str) -> models.SharedHierarchy:
        """Returns all resources you have access to where you don't have access to its parent.
        For example, if you have a access to a shared task, but don't have access to its parent list,
        it will come back in this request.

        Args:
            :team_id (str): The team id to fetch shared hierarchy for.

        Returns:
            :models.SharedHierarchy: Returns an object of type SharedHierarchy.
        """
        model = "team/"
        fetched_hierarchy = self.__get_request(model, team_id, "shared")
        print(fetched_hierarchy)
        if fetched_hierarchy:
            return models.SharedHierarchy.build_shared(fetched_hierarchy)

    # Time Tracking
    def get_time_entries_in_range(
        self,
        team_id: str,
        start_date: str = None,
        end_date: str = None,
        assignees: List[str] = None,
    ) -> models.TimeTrackingData:
        """Gets a list of time tracking entries for a specific date range.

        Args:
            :team_id (str): The id of the team to fetch time entries for.
            :start_date (str, optional): The minimum date to fetch time entries for. Defaults to None.
            :end_date (str, optional): The maximum date to fetch time entries for. Defaults to None.
            :assignees (List[str], optional): A list of user ids to add as assignees. Defaults to None.

        Returns:
            :models.TimeTrackingData: Returns an object of type TimeTrackingData.
        """
        startdate = "start_date="
        enddate = "end_date="
        assignees_temp = "assignee="

        if start_date:
            startdate = f"start_date={fuzzy_time_to_unix(start_date)}"

        if end_date:
            enddate = f"end_date={fuzzy_time_to_unix(end_date)}"

        if assignees:
            if len(assignees) > 1:
                assignees_temp = f'assignee={",".join(assignees)}'

            if len(assignees) == 1:
                assignees_temp = f"assignee={assignees[0]}"

        joined_url = f"time_entries?{startdate}&{enddate}&{assignees_temp}"
        model = "team/"
        fetched_time_data = self.__get_request(model, team_id, joined_url)

        if fetched_time_data:
            return models.TimeTrackingDataList.build_data(fetched_time_data)

    def get_single_time_entry(
        self, team_id: str, timer_id: str
    ) -> models.TimeTrackingData:
        """Gets a single time tracking object.

        Args:
            :team_id (str): The id of the team the time tracking data resides in.
            :timer_id (str): The id of the time entry.

        Returns:
            :models.TimeTrackingData: [Returns an object of type TimeTrackingData.
        """

        model = "team/"
        fetched_time_data = self.__get_request(model, team_id, "time_entries", timer_id)
        print(fetched_time_data)
        if fetched_time_data:
            return models.TimeTrackingDataSingle.build_data(fetched_time_data)

    def start_timer(self, team_id: str, timer_id: str) -> models.TimeTrackingData:
        """start_timer Starts the time tracking timer for a task via a timer id.

        Args:
            :team_id (str): The id of the team the timer exists in.
            :timer_id (str): The id of the timer to start tracking for.

        Returns:
            :models.TimeTrackingData: Returns an object of type TimeTrackingData.
        """
        model = "team/"
        fetched_time_data = self.__post_request(
            model, None, None, False, team_id, "time_entries/start", timer_id
        )

        if fetched_time_data:
            return models.TimeTrackingDataSingle.build_data(fetched_time_data)

    def stop_timer(self, team_id: str) -> models.TimeTrackingData:
        """Stops the time tracking timer for a task via a team id.

        Args:
            :team_id (str): The id of the team the timer exists in.

        Returns:
            :models.TimeTrackingData: Returns an object of type TimeTrackingData.
        """
        model = "team/"
        fetched_time_data = self.__post_request(
            model, None, None, False, team_id, "time_entries/stop"
        )

        if fetched_time_data:
            return models.TimeTrackingDataSingle.build_data(fetched_time_data)
