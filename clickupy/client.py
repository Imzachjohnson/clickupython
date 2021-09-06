import requests
import urllib
from urllib.parse import urlparse
import os
import json
from clickupy import exceptions
from clickupy import helpers
from clickupy import folder
from clickupy import list
from clickupy.helpers import formatting

API_URL = 'https://api.clickup.com/api/v2/'


class ClickUpClient():

    def __init__(self, accesstoken: str, api_url: str = API_URL):
        self.api_url = api_url
        self.accesstoken = accesstoken

    @property
    def _headers(self):
        headers = {'Authorization': self.accesstoken,
                   'Content-Type': 'application/json'}
        return headers

    # Performs a Get request to the ClickUp API
    def _get_request(self, model, *additionalpath):
        path = formatting.url_join(API_URL, model, *additionalpath)
        response = requests.get(path, headers=self._headers)
        response_json = response.json()
        if response.status_code == 401 or response.status_code == 400:
            raise exceptions.ClickupClientError(
                response_json['err'], response.status_code)
        if response.ok:
            return response_json

    # Performs a Post request to the ClickUp API
    def _post_request(self, model, data, *additionalpath):
        path = formatting.url_join(API_URL, model, *additionalpath)
        response = requests.post(path, headers=self._headers, data=data)
        response_json = response.json()
        if response.status_code == 401 or response.status_code == 400:
            raise exceptions.ClickupClientError(
                response_json['err'], response.status_code)
        if response.ok:
            return response_json

    # Performs a Put request to the ClickUp API
    def _put_request(self, model, data, *additionalpath):
        path = formatting.url_join(API_URL, model, *additionalpath)
        response = requests.put(path, headers=self._headers, data=data)
        response_json = response.json()
        if response.status_code == 401 or response.status_code == 400:
            raise exceptions.ClickupClientError(
                response_json['err'], response.status_code)
        if response.ok:
            return response_json

    # Performs a Delete request to the ClickUp API
    def _delete_request(self, model, *additionalpath):
        path = formatting.url_join(API_URL, model, *additionalpath)
        response = requests.delete(path, headers=self._headers)
        if response.ok:
            return response.status_code

    # Fetches a single list item from a given list id and returns a List object
    def get_list(self, list_id: str):
        model = "list/"
        fetched_list = self._get_request(model, list_id)
        final_list = list.SingleList.build_list(fetched_list)
        if response.ok:
            return final_list

    # Fetches all lists from a given folder id and returns a list of List objects
    def get_lists(self, folder_id: str):
        model = "folder/"
        fetched_lists = self._get_request(model, folder_id)
        final_lists = list.AllLists.build_lists(fetched_lists)
        return final_lists

    # Creates and returns a List object in a folder from a given folder ID
    def create_list(self, folder_id: str, name: str, content: str, due_date: str, priority: int, status: str):
        data = {
            'name': name,
            'content': content,
            'due_date': due_date,
            'status': status
        }
        model = "folder/"
        created_list = self._post_request(
            model, json.dumps(data), folder_id, "list")
        if created_list:
            final_list = SingleList.build_list(created_list)
            return final_list

    # Fetches a single folder item from a given folder id and returns a Folder object
    def get_folder(self, folder_id: str):
        model = "folder/"
        fetched_folder = self._get_request(model, folder_id)
        if fetched_folder:
            final_folder = folder.Folder.build_folder(fetched_folder)
            return final_folder

    # Fetches all folders from a given space id and returns a list of Folder objects
    def get_folders(self, space_id: str):
        model = "space/"
        fetched_folders = self._get_request(model, space_id, "folder")
        if fetched_folders:
            final_folders = folder.Folders.build_folders(fetched_folders)
            return final_folders

    # Creates and returns a Folder object in a space from a given space ID
    def create_folder(self, space_id: str, name: str):
        data = {
            'name': name,
        }
        model = "space/"
        created_folder = self._post_request(
            model, json.dumps(data), space_id, "folder")
        if created_folder:
            final_folder = Folder.build_folder(created_folder)
            return final_folder

    # Updates the name of a folder given the folder ID
    def update_folder(self, folder_id: str, name: str):
        data = {
            'name': name,
        }
        model = "folder/"
        updated_folder = self._put_request(
            model, json.dumps(data), folder_id)
        if updated_folder:
            final_folder = Folder.build_folder(updated_folder)
            return final_folder

    # Deletes a folder given a folder ID
    def delete_folder(self, folder_id: str):
        model = "folder/"
        deleted_folder_status = self._delete_request(
            model, folder_id)
