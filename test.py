from clickupy import client

c = client.ClickUpClient("pk_6341704_8OV9MRRLXIK2VO3XV3FNKKLY9IMQAXB3")

# t = c.upload_attachment("1fjav3g", r"C:\Users\Zach\Desktop\me.jpg")


t = c.get_task("1fjav3g")

a = t.upload_attachment(r"C:\Users\Zach\Desktop\me.jpg", c)

print(a.url)