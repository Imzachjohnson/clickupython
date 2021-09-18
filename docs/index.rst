.. clickupy documentation master file, created by
   sphinx-quickstart on Thu Sep 16 19:12:54 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. clickupy documentation master file, created by
   sphinx-quickstart on Thu Sep  9 17:56:55 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Clickupy
====================================
Clickupy is a Python client for the ClickUp API and can be used to interact with the ClickUp API in your projects. ClickUp's API exposes the entire ClickUp infrastructure via a standardized programmatic interface. Using ClickUp's API, you can do just about anything you can do on clickup.com.


Getting started
*****
To start, install clickupy via pip.

::

    $ pip install clickupy


Authentication
*****
There are two ways to authenticate with ClickUp API 2.0, with a personal token or creating an application and authenticating with an OAuth2 flow.

.. note:: IMPORTANT - If you are creating an application for other's to use, it is 
          highly recommended that you use the OAuth2 flow.

Method 1: API Key (Fastest)
---------------
Sign in to ClickUp and navigate to Settings > Apps.
There you will see a an API token. Copy this and save it. You will use this to authenticate the clickupy client with ClickUp's API.

::

    $ from clickupy import ClickUpClient

      API_KEY = 'YOUR API KEY'
      client = ClickUpClient(API_KEY)

      # Example request | Creating a task in a list
      c = client.ClickUpClient(API_KEY)
      task = c.create_task("list_id", name="Test task", due_date="march 2 2021")

      if task:
         print(task.id)