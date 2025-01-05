"""
Django's command-line utility for administrative tasks.
"""
import os
import sys
from django.core.management import execute_from_command_line

def main():
    """
    Run administrative tasks.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

    # Automatically delete and recreate the SQLite database
    db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
    if os.path.exists(db_path):
        print("Deleting existing SQLite database...")
        os.remove(db_path)  # Deletes the SQLite database file

    try:
        # Run migrations to reinitialize the database
        execute_from_command_line(["manage.py", "migrate"])
    except Exception as exc:
        print(f"Error while migrating: {exc}")
        raise

    try:
        execute_from_command_line(sys.argv)
    except Exception as exc:
        print(f"Error while running server: {exc}")
        raise


if __name__ == "__main__":
    main()
