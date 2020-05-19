# coding=utf-8   
import dropbox
from dropbox.files import WriteMode
import datetime
#dbx = dropbox.Dropbox('JUSy-o0vW0gAAAAAAAAAnWt-oe9m54xJMIiK6xoR7aPuUDKdJdCc0_hU1POafwNA')
#dbx.users_get_current_account()
"""
#uploading file
f = open('test1.cpp', 'rb')
dbx.files_upload(f.read(),'/backup/test1.cpp')
f.close()
"""
"""
#downloading file
dbx.files_download_to_file('./backup/miuki.jpg','/43946355.jpg')
"""
"""
# アプリディレクトリにあるファイルの一覧を表示
for entry in dbx.files_list_folder('').entries:
    print(entry.name)
"""
dbx = dropbox.Dropbox('JUSy-o0vW0gAAAAAAAAAnWt-oe9m54xJMIiK6xoR7aPuUDKdJdCc0_hU1POafwNA')
dbx.users_get_current_account()
def writing(words):
    now = datetime.datetime.now()
    dbx.files_download_to_file('log.txt','/backup/log.txt')
    with open("log.txt","a") as f:
        f.write(words+'\t{0:%Y%m%d%H%M%S}\n'.format(now))
    with open('log.txt', 'rb') as f:
        dbx.files_upload(f.read(),'/backup/log.txt',mode=WriteMode('overwrite'))


writing("hello world")