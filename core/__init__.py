# save this as check_versions.py
import django
import daphne
import channels
import asgiref
import psycopg2

def main():
    print("Django version:", django.get_version())
    print("Daphne version:", daphne.__version__)
    print("Channels version:", channels.__version__)
    print("Asgiref version:", asgiref.__version__)
    print("Psycopg2 version:", psycopg2.__version__)

if __name__ == "__main__":
    main()
