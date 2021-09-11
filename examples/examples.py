from clickupy import client


c = client.ClickUpClient("pk_6341704_8OV9MRRLXIK2VO3XV3FNKKLY9IMQAXB3")

t = c.create_task("132216026", name="hello", due_date="march 2 2021")