import logging
import time
import pyrebase

config = {
  "apiKey": "AIzaSyAoL3xv7jSd1turJ_nwLNoh4wrSgmKZBJ4",
  "authDomain": "srmwebedit.firebaseapp.com",
  "databaseURL": "https://srmwebedit-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "srmwebedit",
  "storageBucket": "srmwebedit.appspot.com",
  "messagingSenderId": "509165616130",
  "appId": "1:509165616130:web:09e1a1901161fffcaa7b1b",
  "measurementId": "G-2HXPBMTN25"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log access details
        request_count = db.child("request_count").get().val()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        remote_addr = request.META.get('REMOTE_ADDR')
        method = request.method
        path = request.path
        access_log = f'{timestamp} - {remote_addr} - {method} {path}'
        logging.info(access_log)


        response = self.get_response(request)
        return response
