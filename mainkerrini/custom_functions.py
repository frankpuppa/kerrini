import uuid

media="/srv/www/nginx/media/"

def handle_uploaded_file(file):
    uuidname=uuid.uuid1()
    with open( media + str(uuidname), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)