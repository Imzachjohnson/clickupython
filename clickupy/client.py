import requests
import urllib
from urllib.parse import urlparse
import os
import json
import ntpath
from clickupy import helpers
from clickupy import folder
from clickupy import list
from clickupy import attachment
from clickupy import exceptions
from clickupy import task

from clickupy.helpers import formatting

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
    def _post_request(
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
        response = requests.put(path, headers=self._headers(), data=data)
        response_json = response.json()
        if response.status_code in [401, 400]:
            raise exceptions.ClickupClientError(
                response_json['err'], response.status_code)
        if response.ok:
            return response_json

    # Performs a Delete request to the ClickUp API
    def __delete_request(self, model, *additionalpath):
        path = formatting.url_join(API_URL, model, *additionalpath)
        response = requests.delete(path, headers=self._headers())
        if response.ok:
            return response.status_code

    # Fetches a single list item from a given list id and returns a List object
    def get_list(self, list_id: str):
        if response.ok:
            model = "list/"
            fetched_list = self.__get_request(model, list_id)
            return list.SingleList.build_list(fetched_list)

    # Fetches all lists from a given folder id and returns a list of List objects
    def get_lists(self, folder_id: str):
        model = "folder/"
        fetched_lists = self.__get_request(model, folder_id)
        return list.AllLists.build_lists(fetched_lists)

    # Creates and returns a List object in a folder from a given folder ID
    def create_list(
            self,
            folder_id: str,
            name: str,
            content: str,
            due_date: str,
            priority: int,
            status: str):
        data = {
            'name': name,
            'content': content,
            'due_date': due_date,
            'status': status
        }
        model = "folder/"
        created_list = self.post_request(
            model, json.dumps(data), folder_id, "list")
        if created_list:
            return SingleList.build_list(created_list)

    def get_folder(self, folder_id: str) -> folder.Folder:
        """Fetches a single folder item from a given folder id and returns a Folder object.

        Args:
            folder_id (str): The ID of the ClickUp folder to retrieve.

        Returns:
            Folder: Returns a single Folder object.
        """
        model = "folder/"
        fetched_folder = self.__get_request(model, folder_id)
        if fetched_folder:
            return folder.Folder.build_folder(fetched_folder)

    def get_folders(self, space_id: str) -> folder.Folders:
        """Fetches all folders from a given space ID and returns a list of Folder objects.

        Args:
            space_id (str): The ID of the ClickUp space to retrieve the list of folder from.

        Returns:
            Folders: Returns a list of Folder objects.
        """
        model = "space/"
        fetched_folders = self.__get_request(model, space_id, "folder")
        if fetched_folders:
            return folder.Folders.build_folders(fetched_folders)

    def create_folder(self, space_id: str, name: str) -> folder.Folder:
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
        created_folder = self.post_request(
            model, json.dumps(data), space_id, "folder")
        if created_folder:
            return Folder.build_folder(created_folder)

    def update_folder(self, folder_id: str, name: str) -> folder.Folder:
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
            return Folder.build_folder(updated_folder)

    def delete_folder(self, folder_id: str) -> None:
        """Deletes a folder from a given folder ID.

        Args:
            folder_id (str): The ID of the ClickUp folder to delete.
        """
        model = "folder/"
        deleted_folder_status = self.__delete_request(
            model, folder_id)

    def upload_attachment(
            self,
            task_id: str,
            file_path: str) -> attachment.Attachment:
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
                uploaded_attachment = self.post_request(
                    model, data, files, True, "attachment")

                if uploaded_attachment:
                    final_attachment = attachment.build_attachment(
                        uploaded_attachment)
                return final_attachment

    def get_task(self, task_id: str) -> task.Task:
        """Fetches a single ClickUp task item and returns a Task object.

        Args:
            task_id (str): The ID of the task to return.

        Returns:
            Task: Returns an object of type Task.
        """
        model = "task/"
        fetched_task = self.__get_request(model, task_id)
        final_task = task.Task.build_task(fetched_task)
        if final_task:
            return final_task
