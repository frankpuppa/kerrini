def handle_uploaded_file(f,filename):
    with open('/srv/www/nginx/media/'+filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)