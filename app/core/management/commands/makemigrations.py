from django.core.management.commands.makemigrations import Command as MakeMigrationsCommand
from django.db.migrations.operations.models import CreateModel
from django.db.migrations.operations.base import Operation
from django.db.migrations.writer import MigrationWriter
import os
import re

class CreateUpdatedAtTrigger(Operation):
    reversible = True
    
    def __init__(self, table_name):
        self.table_name = table_name
    
    def state_forwards(self, app_label, state):
        pass
    
    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        schema_editor.execute(
            f"CREATE TRIGGER updated_at_{self.table_name} BEFORE UPDATE ON {self.table_name} FOR EACH ROW EXECUTE PROCEDURE updated_at_column()"
        )
    
    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        schema_editor.execute(f"DROP TRIGGER IF EXISTS updated_at_{self.table_name} ON {self.table_name}")
    
    def describe(self):
        return f"Create updated_at trigger for {self.table_name}"

class Command(MakeMigrationsCommand):
		def write_migration_files(self, changes):
				for app_label, migrations_list in changes.items():
						for migration in migrations_list:
								self.add_triggers_to_migration(migration)
				
				super().write_migration_files(changes)

		def add_triggers_to_migration(self, migration):
				"""Add trigger operations after CreateModel operations"""
				new_operations = []
				
				for operation in migration.operations:
						new_operations.append(operation)
						
						if isinstance(operation, CreateModel):
								from django.db import models
								
								model_options = operation.options
								table_name = model_options.get('db_table')
								
								if not table_name:
										table_name = f"{migration.app_label}_{operation.name.lower()}"
								
								trigger_op = CreateUpdatedAtTrigger(table_name)
								new_operations.append(trigger_op)
								print(f"Added trigger for table: {table_name}")
				
				migration.operations = new_operations
