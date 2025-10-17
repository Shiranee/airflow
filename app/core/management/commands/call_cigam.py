from django.core.management.base import BaseCommand
from store.services.import_stores import CigamStores
from employee.services.import_employees import CigamEmployee


class Command(BaseCommand):
    '''Handler for Cigam data'''

    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            required=True,
            help='Specify what to import (any string is allowed)'
        )

    def handle(self, *args, **options):
        import_type = options['type']
        
        if import_type == 'stores':
            result = CigamStores().run_cigam_stores()
            self.stdout.write(self.style.SUCCESS("Cigam Stores imported successfully"))
        elif import_type == 'employees':
            result = CigamEmployee().run_cigam_employees()
            print(result)
            self.stdout.write(self.style.SUCCESS("Cigam Employees imported successfully"))
