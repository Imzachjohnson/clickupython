from clickupy import client

c = client.ClickUpClient("pk_6341704_8OV9MRRLXIK2VO3XV3FNKKLY9IMQAXB3")


t = c.get_folder("72233211")


print(t)