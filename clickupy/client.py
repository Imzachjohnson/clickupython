import requests
import urllib
from urllib.parse import urlparse
import os
import json
import ntpath
from typing import List, Optional


from clickupy.helpers.timefuncs import fuzzy_time_to_seconds, fuzzy_time_to_unix
from clickupy.helpers import formatting
from clickupy import models
from clickupy import exceptions


API_URL = 'https://api.clickup.com/api/v2/'


class ClickUpClient():

    def __init__(self, accesstoken: str, api_url: str = API_URL):
        self.api_url = api_url
        self.accesstoken = accesstoken

    def __headers(self, file_upload: bool = False):

        return (
            {'Authorization': self.accesstoken}
            if file_upload
            else {
                'Authorization': self.accesstoken,
                'Content-Type': 'application/json',
            }
        )

    # Performs a Get request to the ClickUp API
    def __get_request(self, model, *additionalpath):

        path = formatting.url_join(API_URL, model, *additionalpath)
        response = requests.get(path, headers=self.__headers())
        response_json = response.json()
        if response.status_code == 429:
            raise exceptions.ClickupClientError(
                "Rate limit exceeded", response.status_code)
        if response.status_code in [401, 400]:
            raise exceptions.ClickupClientError(
                response_json['err'], response.status_code)
        if response.ok:
            return response_json

    # Performs a Post request to the ClickUp API
    def __post_request(
            self,
            model,
            data,
            upload_files=None,
            file_upload=False,
            *additionalpath):
        path = formatting.url_join(API_URL, model, *additionalpath)

        if upload_files:
            response = requests.post(path, headers=self.__headers(
                True), data=data, files=upload_files)
        else:
            response = requests.post(
                path, headers=self.__headers(), data=data)
        response_json = response.json()

        if response.status_code in [401, 400, 500]:
            raise exceptions.ClickupClientError(
                response_json['err'], response.status_code)
        if response.ok:
            return response_json

    # Performs a Put request to the ClickUp API
    def __put_request(self, model, data, *additionalpath):
        path = formatting.url_join(API_URL, model, *additionalpath)
        response = requests.put(path, headers=self.__headers(), data=data)
        response_json = response.json()
        if response.status_code in [401, 400]:
            raise exceptions.ClickupClientError(
                response_json['err'], response.status_code)
        if response.ok:
            return response_json

    # Performs a Delete request to the ClickUp API
    def __delete_request(self, model, *additionalpath):
        path = formatting.url_join(API_URL, model, *additionalpath)
        response = requests.delete(path, headers=self.__headers())
        if response.ok:
            return response.status_code
        else:
            raise exceptions.ClickupClientError(
                response_json['err'], response.status_code)

    # Lists
    def get_list(self, list_id: str) -> models.SingleList:
        """Fetches a single list item from a given list id and returns a List object.

        Args:
            list_id (str): The ID od the ClickUp list to be returned.

        Returns:
            clickuplist.SingleList: Returns a list of type List.
        """
        model = "list/"
        fetched_list = self.__get_request(model, list_id)

        return models.SingleList.build_list(fetched_list)

    def get_lists(self, folder_id: str) -> models.AllLists:
        """Fetches all lists from a given folder id and returns a list of List objects.

        Args:
            folder_id (str): The ID od the ClickUp folder to be returned.

        Returns:
            list.AllLists: Returns a list of type AllLists.
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
            status: str) -> models.SingleList:
        """Creates and returns a List object in a folder from a given folder ID.

        Args:
            folder_id (str): The ID of the ClickUp folder.
            name (str): The name of the created list.
            content (str): The description content of the created list.
            due_date (str): The due date of the created list.
            priority (int): An integer 1 : Urgent, 2 : High, 3 : Normal, 4 : Low.
            status (str): Refers to the List color rather than the task Statuses available in the List.

        Returns:
            list.SingleList: Returns an object of type SingleList.
        """
        data = {
            'name': name,
            'content': content,
            'due_date': due_date,
            'status': status
        }
        model = "folder/"
        created_list = self.__post_request(
            model, json.dumps(data), None, False, folder_id, "list")
        if created_list:
            return models.SingleList.build_list(created_list)

    # Folders
    def get_folder(self, folder_id: str) -> models.Folder:
        """Fetches a single folder item from a given folder id and returns a Folder object.

        Args:
            folder_id (str): The ID of the ClickUp folder to retrieve.

        Returns:
            Folder: Returns an object of type Folder.
        """
        model = "folder/"
        fetched_folder = self.__get_request(model, folder_id)
        if fetched_folder:
            return models.Folder.build_folder(fetched_folder)

    def get_folders(self, space_id: str) -> models.Folders:
        """Fetches all folders from a given space ID and returns a list of Folder objects.

        Args:
            space_id (str): The ID of the ClickUp space to retrieve the list of folder from.

        Returns:
            Folders: Returns a list of Folder objects.
        """
        model = "space/"
        fetched_folders = self.__get_request(model, space_id, "folder")
        if fetched_folders:
            return models.Folders.build_folders(fetched_folders)

    def create_folder(self, space_id: str, name: str) -> models.Folder:
        """Creates and returns a Folder object in a space from a given space ID.

        Args:
            space_id (str): The ID of the ClickUp space to create the folder inside.
            name (str): String value that the created folder will utilize as its name.

        Returns:
            Folder: Returns the created Folder object.
        """
        data = {
            'name': name,
        }
        model = "space/"
        created_folder = self.__post_request(
            model, json.dumps(data), None, False, space_id, "folder")
        if created_folder:
            return models.Folder.build_folder(created_folder)

    def update_folder(self, folder_id: str, name: str) -> models.Folder:
        """Updates the name of a folder given the folder ID.

        Args:
            folder_id (str): The ID of the ClickUp folder to update.
            name (str): String that the folder name will be updated to reflect.

        Returns:
            Folder: Returns the updated Folder as an object.
        """
        data = {
            'name': name,
        }
        model = "folder/"
        updated_folder = self.__put_request(
            model, json.dumps(data), folder_id)
        if updated_folder:
            return models.Folder.build_folder(updated_folder)

    def delete_folder(self, folder_id: str) -> None:
        """Deletes a folder from a given folder ID.

        Args:
            folder_id (str): The ID of the ClickUp folder to delete.
        """
        model = "folder/"
        deleted_folder_status = self.__delete_request(
            model, folder_id)
        return(True)

    # Tasks

    def upload_attachment(
            self,
            task_id: str,
            file_path: str) -> models.Attachment:
        """Uploads an attachment to a ClickUp task.

        Args:
            task_id (str): The ID of the task to upload to.
            file_path (str): The filepath of the file to upload.

        Returns:
            Attachment: Returns an attachment object.
        """

        if os.path.exists(file_path):

            with open(file_path, 'rb') as f:
                files = [
                    ('attachment', (f.name, open(
                        file_path, 'rb')))
                ]
                data = {'filename': ntpath.basename(f.name)}
                model = "task/" + task_id
                uploaded_attachment = self.__post_request(
                    model, data, files, True, "attachment")

                if uploaded_attachment:
                    final_attachment = models.Attachment.build_attachment(
                        uploaded_attachment)
                return final_attachment

    def get_task(self, task_id: str) -> models.Task:
        """Fetches a single ClickUp task item and returns a Task object.

        Args:
            task_id (str): The ID of the task to return.

        Returns:
            Task: Returns an object of type Task.
        """
        model = "task/"
        fetched_task = self.__get_request(model, task_id)
        final_task = models.Task.build_task(fetched_task)
        if final_task:
            return final_task

    def get_tasks(self, list_id: str) -> models.Tasks:
        """Fetches a list of task items from a given list ID.

        Args:
            list_id (str): The ID of the ClickUp list to fetch tasks from.

        Returns:
            task.Tasks: Returns an object of type Tasks.
        """
        model = "list/"
        fetched_tasks = self.__get_request(model, list_id, "task")

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
            notify_all: bool = True) -> models.Task:

        if priority and priority not in range(1, 4):
            raise exceptions.ClickupClientError(
                "Priority must be in range of 0-4.", "Priority out of range")
        if due_date:
            due_date = fuzzy_time_to_unix(due_date)

        arguments = {}
        arguments.update(vars())
        arguments.pop('self', None)
        arguments.pop('arguments', None)
        arguments.pop('list_id', None)

        final_dict = json.dumps(
            {k: v for k, v in arguments.items() if v is not None})

        model = "list/"
        created_task = self.__post_request(
            model, final_dict, None, False, list_id, "task")

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
            remove_assignees: List[int] = None) -> models.Task:
        """[summary]

        Args:
            task_id ([type]): The ID of the ClickUp task to update.
            name (str, optional): Sting value to update the task name to. Defaults to None.
            description (str, optional): Sting value to update the task description to. Defaults to None.
            status (str, optional): String value of the tasks status. Defaults to None.
            priority (int, optional): Priority of the task. Range 1-4. Defaults to None.
            time_estimate (int, optional): Time estimate of the task. Defaults to None.
            archived (bool, optional): Whether the task should be archived or not. Defaults to None.
            add_assignees (List[str], optional): List of assignee IDs to add to the task. Defaults to None.
            remove_assignees (List[int], optional): List of assignee IDs to remove from the task. Defaults to None.

        Raises:
            exceptions.ClickupClientError: Raises "Priority out of range" exception for invalid priority range.

        Returns:
            task.Task: Returns an object of type Task.
        """
        if priority and priority not in range(1, 4):
            raise exceptions.ClickupClientError(
                "Priority must be in range of 0-4.", "Priority out of range")

        arguments = {}
        arguments.update(vars())
        arguments.pop('self', None)
        arguments.pop('arguments', None)
        arguments.pop('task_id', None)
        arguments.pop('add_assignees', None)
        arguments.pop('remove_assignees', None)

        if add_assignees and remove_assignees:
            arguments.update(
                {'assignees': {'add': add_assignees, 'rem': remove_assignees}})
        elif add_assignees:
            arguments.update({'assignees': {'add': add_assignees}})
        elif remove_assignees:
            arguments.update({'assignees': {'rem': remove_assignees}})

        final_dict = json.dumps(
            {k: v for k, v in arguments.items() if v is not None})

        model = "task/"
        updated_task = self.__put_request(
            model, final_dict, task_id)
        if updated_task:
            return models.Task.build_task(updated_task)

    def delete_task(self, task_id: str) -> None:
        """Deletes a task from a given task ID.

        Args:
            folder_id (str): The ID of the ClickUp task to delete.
        """
        model = "task/"
        deleted_task_status = self.__delete_request(
            model, task_id)
        return(True)

    # Comments
    def get_task_comments(self, task_id: str):

        model = "task/"
        fetched_comments = self.__get_request(model, task_id, "comment")
        final_comments = models.Comments.build_comments(fetched_comments)
        if final_comments:
            return final_comments

    def get_list_comments(self, list_id: str):

        model = "list/"
        fetched_comments = self.__get_request(model, list_id, "comment")
        final_comments = models.Comments.build_comments(fetched_comments)
        if final_comments:
            return final_comments

    def get_chat_comments(self, view_id: str):

        model = "view/"
        fetched_comments = self.__get_request(model, view_id, "comment")
        final_comments = models.Comments.build_comments(fetched_comments)
        if final_comments:
            return final_comments

    def update_comment(
            self,
            comment_id: str,
            comment_text: str = None,
            assignee: str = None,
            resolved: bool = None) -> models.Comment:

        arguments = {}
        arguments.update(vars())
        arguments.pop('self', None)
        arguments.pop('arguments', None)
        arguments.pop('comment_id', None)

        model = "comment/"

        final_dict = json.dumps(
            {k: v for k, v in arguments.items() if v is not None})

        updated_comment = self.__put_request(
            model, final_dict, comment_id)
        if updated_comment:
            return True

    def delete_comment(self, comment_id: str) -> bool:

        model = "comment/"
        deleted_comment_status = self.__delete_request(
            model, comment_id)
        return(True)

    def create_task_comment(
            self,
            task_id: str,
            comment_text: str,
            assignee: str = None,
            notify_all: bool = True) -> models.Comment:

        arguments = {}
        arguments.update(vars())
        arguments.pop('self', None)
        arguments.pop('arguments', None)
        arguments.pop('task_id', None)

        model = "task/"

        final_dict = json.dumps(
            {k: v for k, v in arguments.items() if v is not None})

        created_comment = self.__post_request(
            model, final_dict, None, False, task_id, "comment")

        final_comment = models.Comment.build_comment(created_comment)
        if final_comment:
            return final_comment

    # Teams
    def get_teams(self):

        model = "team/"
        fetched_teams = self.__get_request(model)
        final_teams = teams.Teams.build_teams(fetched_teams)
        if final_teams:
            return final_teams

    # Checklists
    def create_checklist(self, task_id: str, name: str):

        data = {
            'name': name,
        }

        model = "task/"
        created_checklist = self.__post_request(
            model, json.dumps(data), None, False, task_id, "checklist")
        return models.Checklists.build_checklist(created_checklist)

    def create_checklist_item(
            self,
            checklist_id: str,
            name: str,
            assignee: str = None):

        data = {}

        data = {
            'name': name,
            'assignee': assignee
        } if assignee else {
            'name': name
        }
        model = "checklist/"
        created_checklist = self.__post_request(
            model, json.dumps(data), None, False, checklist_id, "checklist_item")
        return models.Checklists.build_checklist(created_checklist)

    def update_checklist(self, checklist_id: str, name: str = None, postion: int = None):

        if not name and not postion:
            return

        data = {}

        if name:
            data.update({'name': name})
        if postion:
            data.update({'postition': position})

        model = "checklist/"
        updated_checklist = self.__put_request(
            model, json.dumps(data), checklist_id)
        if updated_checklist:
            return models.Checklists.build_checklist(updated_checklist)

    def delete_checklist(self, checklist_id: str) -> None:

        model = "checklist/"
        self.__delete_request(
            model, checklist_id)
        return(True)

    def delete_checklist_item(self, checklist_id: str, checklist_item_id: str) -> None:
        """test summary

        Args:
            checklist_id (str): [description]
            checklist_item_id (str): [description]
        """        
        model = "checklist/"
        self.__delete_request(
            model, checklist_id, "checklist_item", checklist_item_id)
        return(True)

    def update_checklist_item(self, checklist_id: str, checklist_item_id: str, name: str = None, resolved: bool = None, parent:str = None):
        

        arguments = {}
        arguments.update(vars())
        arguments.pop('self', None)
        arguments.pop('arguments', None)
        arguments.pop('checklist_id', None)
        arguments.pop('checklist_item_id', None)

        model = "checklist/"

        final_dict = json.dumps(
            {k: v for k, v in arguments.items() if v is not None})

        item_update = self.__put_request(
            model, final_dict, checklist_id, "checklist_item", checklist_item_id)

        final_update = models.Checklists.build_checklist(item_update)
        if final_update:
            return final_update


    # Members
    def get_task_members(
            self,
            task_id: str):

        model = "task/"
        
        task_members = self.__get_request(model, task_id, "member")
        return models.Members.build_members(task_members)

    def get_list_members(
            self,
            list_id: str):
            
        model = "list/"
        
        task_members = self.__get_request(model, list_id, "member")
        return models.Members.build_members(task_members)

    # Tags

    