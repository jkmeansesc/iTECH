import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iTECH.settings')

import django
django.setup()
# from authentication.models import User

def populate():
    pass

if __name__ == '__main__':
    print("populating blog...")
    populate()
    print("populating complete")

