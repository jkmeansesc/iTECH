import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iTECH.settings')

import django
django.setup()
from authentication.models import User

def populate():
    user1 = User(username="user1", password="user1", email="user1@student.gla.ac.uk")
    user1.save()
    user2 = User(username="user2", password="user2", email="user2@student.gla.ac.uk")
    user2.save()
    user3 = User(username="user3", password="user3", email="user3@student.gla.ac.uk")
    user3.save()

if __name__ == '__main__':
    print("populating authentication...")
    populate()
    print("populating complete")

