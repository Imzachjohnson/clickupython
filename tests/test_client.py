# tests/tests_clickup.py
from unittest import mock
from clickupy.models import Folders,AssignedBy, Task, Comment, AllLists, SingleList, Tasks, Asssignee
import pytest
import os
import sys

from clickupy import client
from clickupy import models

API_KEY = "pk_6341704_8OV9MRRLXIK2VO3XV3FNKKLY9IMQAXB3"
MOCK_API_URL = "https://private-anon-3a942619a6-clickup20.apiary-mock.com/api/v2/"


class TestClientLists():

    @pytest.mark.lists
    def test_get_list(self):

        c = client.ClickUpClient(API_KEY)
        result = c.get_list("132237389")
        assert type(result) == SingleList
        assert result.id == "132237389"

    @mock.patch("clickupy.client.API_URL", MOCK_API_URL)
    def test_get_lists(self):

        c = client.ClickUpClient(API_KEY)
        result = c.get_lists("456")

        assert isinstance(result, models.AllLists)

    # Work on this test
    @mock.patch("clickupy.client.API_URL", MOCK_API_URL)
    def test_create_list(self):

        c = client.ClickUpClient(API_KEY)
        result = c.create_list("456", "New List Name",
                               "New List Content", "1567780450202", 2361428, "red")

        assert result.id == "124"
        assert result.assignee.id == '183'
        assert result.folder.id == '456'
        assert result.space.id == '789'
        assert len(result.statuses) > 0
        assert result.statuses[0].status == "to do"

        assert isinstance(result, models.SingleList)


class TestClientFolders():
    @mock.patch("clickupy.client.API_URL", MOCK_API_URL)
    @pytest.mark.folders
    def test_get_folder(self):

        c = client.ClickUpClient(API_KEY)
        result = c.get_folder("457")
        assert result.id == "457"
        assert result.name == "Updated Folder Name"
        assert result.task_count == 0
        assert isinstance(result, models.Folder)

    @pytest.mark.folders
    def test_get_folders(self):

        c = client.ClickUpClient(API_KEY)
        result = c.get_folders("30067535")
        assert len(result.folders) > 0
        assert result.folders[0].id == "72245695"
        assert isinstance(result, models.Folders)

    @mock.patch("clickupy.client.API_URL", MOCK_API_URL)
    @pytest.mark.folders
    def test_create_folder(self):

        c = client.ClickUpClient(API_KEY)
        result = c.create_folder("789", "New Folder Name")

        assert result.id == "457"
        assert result.name == "New Folder Name"
        assert result.hidden == False
        assert result.space.id == 789
        assert result.task_count == 0
        assert isinstance(result, models.Folder)
        


    @mock.patch("clickupy.client.API_URL", MOCK_API_URL)
    @pytest.mark.folders
    def test_update_folder(self):

        c = client.ClickUpClient(API_KEY)
        result = c.update_folder("457", "Updated Folder Name")

        assert result.id == "457"
        assert result.name == "Updated Folder Name"
        assert result.hidden == False
        assert result.space.id == 789
        assert result.task_count == 0
        assert isinstance(result, models.Folder)

    @mock.patch("clickupy.client.API_URL", MOCK_API_URL)
    @pytest.mark.folders
    def test_delete_folder(self):

        c = client.ClickUpClient(API_KEY)
        result = c.delete_folder("457")

        assert result


class TestClientTasks():
    @mock.patch("clickupy.client.API_URL", MOCK_API_URL)
    @pytest.mark.tasks
    def test_upload_attachment(self):

        c = client.ClickUpClient(API_KEY)
        result = c.upload_attachment(
            "9hv", r"C:\Users\Zach\Desktop\me.jpg")

        assert result.id == "ac434d4e-8b1c-4571-951b-866b6d9f2ee6.png"
        assert result.version == 0
        assert result.date == "1569988578766"
        assert type(result) == models.Attachment
        assert result.title == "image.png"
        assert result.extension == "png"
        assert result.thumbnail_small == "https://attachments-public.clickup.com/ac434d4e-8b1c-4571-951b-866b6d9f2ee6/logo_small.png"
        assert result.thumbnail_large == "https://attachments-public.clickup.com/ac434d4e-8b1c-4571-951b-866b6d9f2ee6/logo_small.png"
        assert result.url == "https://attachments-public.clickup.com/ac434d4e-8b1c-4571-951b-866b6d9f2ee6/logo_small.png"

    @pytest.mark.tasks
    def test_create_task(self):

        c = client.ClickUpClient(API_KEY)
        result = c.create_task(
            "132235954", "New Task Name", "New Task Description")

        assert isinstance(result, models.Task)

    @pytest.mark.tasks
    def test_get_tasks(self):

        c = client.ClickUpClient(API_KEY)
        result = c.get_tasks("132211116")
        assert isinstance(result, models.Tasks)

    @pytest.mark.tasks
    def test_update_task(self):

        description = "Updated Task description"

        c = client.ClickUpClient(API_KEY)
        result = c.update_task("1g3b7k6", description=description)
        assert type(result) == models.Task
        assert result.description == description


class TestClientComments():
    @pytest.mark.comments
    def test_get_task_comments(self):
        c = client.ClickUpClient(API_KEY)
        result = c.get_task_comments("1gexdjy")

        for c in result:
            assert c.user.id == "6341704"