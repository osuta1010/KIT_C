from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)
"""
f = drive.CreateFile({'title': 'test.jpg', 'mimeType': 'image/jpeg'})
print(f.SetContentFile('test.jpg'))
print(f.Upload())
"""

file_list = drive.ListFile().GetList()
for f in file_list:
    if f['title'] == "DSC_0161.JPG":
        print(f['title'], f['id'])