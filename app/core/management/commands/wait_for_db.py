import time

from django.db import connection
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command that waits for database to be available"""

    def handle(self, *args, **options):
        """Handle the command"""
        self.stdout.write('Waiting for database...')
        db_conn = None
        wait_time = 1
        while not db_conn:
            try:
                connection.ensure_connection()
                db_conn = True
            except OperationalError:
                self.stdout.write(
                    f'Database unavailable, waiting {wait_time} second(s)...')
                time.sleep(wait_time)
                wait_time += 1

        self.stdout.write(self.style.SUCCESS('Database available!'))
