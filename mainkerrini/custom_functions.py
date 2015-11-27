import uuid
import magic
from django.contrib.staticfiles.management.commands import collectstatic
import shutil

def handle_uploaded_file(src,dest):
    media="/srv/www/nginx/kerrini/mainkerrini/static/videos/" + dest + "/"
    filename=uuid.uuid1()
    with open( media + str(filename), 'wb+') as destination:
        for chunk in src.chunks():
            destination.write(chunk)
    return filename


def move_file(src,dst):
    filename=uuid.uuid1()
    media="/srv/www/nginx/kerrini/mainkerrini/static/videos/" + dst + "/" +str(filename)
    shutil.move(src, media)
    return filename