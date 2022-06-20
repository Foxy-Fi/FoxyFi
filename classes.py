from firebase_db import *


class FirebaseDB:
    def __init__(self):
        auth, db = initialize_firebase_db()
        self.auth = auth
        self.db = db
