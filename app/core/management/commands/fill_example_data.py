from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    """Django command that waits for database to be available"""

    def handle(self, *args, **options):
        """Handle the command"""
        call_command('loaddata', 'example_data_fixture.json')

        self.stdout.write(self.style.SUCCESS('Example data inserted!'))
        self.stdout.write(self.style.SUCCESS(
            'Login with admin@example.com::admin'))
