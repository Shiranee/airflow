'''
A module for testing models data insertions.
'''
import requests
import json
from typing import Dict, List, Any, Optional
from django.db import models
from django.apps import apps
import logging

logger = logging.getLogger(__name__)

class MockarooDataGenerator:
    """
    Generic function to generate mock data for Django models using Mockaroo API
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the Mockaroo data generator
        
        Args:
            api_key (str): Your Mockaroo API key
        """
        self.api_key = api_key
        self.base_url = "https://api.mockaroo.com/api/generate.json"
        
        # Mapping Django field types to Mockaroo types
        self.field_type_mapping = {
            'AutoField': {'type': 'Row Number', 'min': 1, 'max': 1000000},
            'BigAutoField': {'type': 'Row Number', 'min': 1, 'max': 1000000},
            'BigIntegerField': {'type': 'Number', 'min': -9223372036854775808, 'max': 9223372036854775807},
            'BooleanField': {'type': 'Boolean'},
            'CharField': {'type': 'Full Name'},  # Default, will be customized based on field name
            'DateField': {'type': 'Date', 'min': '1/1/2020', 'max': '12/31/2024'},
            'DateTimeField': {'type': 'Datetime', 'min': '1/1/2020', 'max': '12/31/2024'},
            'DecimalField': {'type': 'Money'},
            'EmailField': {'type': 'Email Address'},
            'FloatField': {'type': 'Number', 'min': 0, 'max': 1000000, 'decimals': 2},
            'IntegerField': {'type': 'Number', 'min': 0, 'max': 2147483647},
            'PositiveIntegerField': {'type': 'Number', 'min': 1, 'max': 2147483647},
            'PositiveSmallIntegerField': {'type': 'Number', 'min': 1, 'max': 32767},
            'SmallIntegerField': {'type': 'Number', 'min': -32768, 'max': 32767},
            'TextField': {'type': 'Sentences', 'min': 1, 'max': 3},
            'TimeField': {'type': 'Time'},
            'URLField': {'type': 'URL'},
            'UUIDField': {'type': 'GUID'},
            'ForeignKey': {'type': 'Number', 'min': 1, 'max': 100},  # Will reference existing IDs
        }
        
        # Custom field mappings based on field names
        self.field_name_mapping = {
            'cnpj': {'type': 'Regular Expression', 'value': r'\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}'},
            'phone': {'type': 'Phone'},
            'whatsapp': {'type': 'Phone'},
            'email': {'type': 'Email Address'},
            'url': {'type': 'URL'},
            'instagram': {'type': 'Custom List', 'values': [
                'https://instagram.com/store1', 'https://instagram.com/store2',
                'https://instagram.com/store3', 'https://instagram.com/store4'
            ]},
            'name': {'type': 'Company Name'},
            'name_comercial': {'type': 'Company Name'},
            'name_legal': {'type': 'Company Name'},
            'working_days': {'type': 'Custom List', 'values': [
                'Monday-Friday', 'Monday-Saturday', 'Monday-Sunday', 'Tuesday-Saturday'
            ]},
            'working_hours': {'type': 'Custom List', 'values': [
                '9am-6pm', '8am-8pm', '10am-10pm', '9am-5pm', '24 hours'
            ]},
            'cover_photo': {'type': 'Custom List', 'values': [
                'https://picsum.photos/800/400?random=1',
                'https://picsum.photos/800/400?random=2',
                'https://picsum.photos/800/400?random=3'
            ]},
            'store_photo': {'type': 'Custom List', 'values': [
                'https://picsum.photos/400/400?random=1',
                'https://picsum.photos/400/400?random=2',
                'https://picsum.photos/400/400?random=3'
            ]},
        }

    def get_mockaroo_field_config(self, field: models.Field, field_name: str) -> Dict[str, Any]:
        """
        Convert Django field to Mockaroo field configuration
        
        Args:
            field: Django model field
            field_name: Name of the field
            
        Returns:
            Dict containing Mockaroo field configuration
        """
        field_type = field.__class__.__name__
        config = {'name': field_name}
        
        # Check if field name has specific mapping
        for name_pattern, name_config in self.field_name_mapping.items():
            if name_pattern.lower() in field_name.lower():
                config.update(name_config)
                return config
        
        # Use field type mapping
        if field_type in self.field_type_mapping:
            config.update(self.field_type_mapping[field_type])
        else:
            # Default to text for unknown field types
            config.update({'type': 'Full Name'})
        
        # Handle CharField max_length
        if hasattr(field, 'max_length') and field.max_length:
            if config.get('type') == 'Full Name':
                if field.max_length < 50:
                    config['type'] = 'First Name'
                elif field.max_length > 200:
                    config['type'] = 'Sentences'
                    config['min'] = 1
                    config['max'] = 2
        
        # Handle null and blank fields
        if field.null or field.blank:
            config['percent_blank'] = 20  # 20% chance of being blank
            
        return config

    def generate_schema_for_model(self, model_class: models.Model, exclude_fields: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Generate Mockaroo schema for a Django model
        
        Args:
            model_class: Django model class
            exclude_fields: List of field names to exclude
            
        Returns:
            List of Mockaroo field configurations
        """
        if exclude_fields is None:
            exclude_fields = ['created_at', 'updated_at', 'deleted_at']
            
        schema = []
        
        for field in model_class._meta.fields:
            if field.name in exclude_fields:
                continue
                
            # Skip auto-generated timestamp fields that have db_default
            if hasattr(field, 'db_default') and field.db_default and 'at' in field.name:
                continue
                
            field_config = self.get_mockaroo_field_config(field, field.name)
            schema.append(field_config)
            
        return schema

    def generate_mock_data(self, model_class: models.Model, count: int = 10, 
                          exclude_fields: Optional[List[str]] = None,
                          custom_schema: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
        """
        Generate mock data for a Django model using Mockaroo API
        
        Args:
            model_class: Django model class
            count: Number of records to generate (max 1000 for free accounts)
            exclude_fields: List of field names to exclude
            custom_schema: Custom Mockaroo schema (overrides auto-generated schema)
            
        Returns:
            List of dictionaries containing mock data
        """
        try:
            # Generate or use custom schema
            if custom_schema:
                schema = custom_schema
            else:
                schema = self.generate_schema_for_model(model_class, exclude_fields)
            
            # Prepare request payload
            payload = {
                'key': self.api_key,
                'count': min(count, 1000),  # Mockaroo free limit
                'array': True,
                'fields': schema
            }
            
            # Make API request
            response = requests.post(self.base_url, json=payload, timeout=30)
            response.raise_for_status()
            
            mock_data = response.json()
            logger.info(f"Generated {len(mock_data)} mock records for {model_class.__name__}")
            
            return mock_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Mockaroo API: {e}")
            raise
        except Exception as e:
            logger.error(f"Error generating mock data: {e}")
            raise

    def create_model_instances(self, model_class: models.Model, mock_data: List[Dict[str, Any]], 
                             bulk_create: bool = True, related_objects_cache: Optional[Dict] = None) -> List[models.Model]:
        """
        Create Django model instances from mock data with proper foreign key handling
        
        Args:
            model_class: Django model class
            mock_data: List of dictionaries containing mock data
            bulk_create: Whether to use bulk_create for better performance
            related_objects_cache: Cache of related objects to avoid repeated queries
            
        Returns:
            List of created model instances
        """
        if related_objects_cache is None:
            related_objects_cache = {}
            
        instances = []
        
        # Pre-fetch related objects for foreign keys
        foreign_key_objects = {}
        for field in model_class._meta.fields:
            if isinstance(field, models.ForeignKey):
                related_model = field.related_model
                cache_key = related_model.__name__
                
                if cache_key not in related_objects_cache:
                    related_objects_cache[cache_key] = list(related_model.objects.all())
                
                foreign_key_objects[field.name] = related_objects_cache[cache_key]
        
        for i, data in enumerate(mock_data):
            # Filter out fields that don't exist in the model
            model_fields = {f.name for f in model_class._meta.fields}
            filtered_data = {k: v for k, v in data.items() if k in model_fields}
            
            # Handle foreign key fields with proper distribution
            for field in model_class._meta.fields:
                if isinstance(field, models.ForeignKey) and field.name in filtered_data:
                    related_objects = foreign_key_objects.get(field.name, [])
                    
                    if related_objects:
                        # Distribute related objects more evenly
                        # Use modulo to cycle through available objects
                        related_instance = related_objects[i % len(related_objects)]
                        filtered_data[field.name] = related_instance
                    else:
                        logger.warning(f"No related objects found for {field.name}")
                        # Remove the foreign key field if no related object exists
                        if field.name in filtered_data:
                            del filtered_data[field.name]
            
            try:
                instance = model_class(**filtered_data)
                instances.append(instance)
            except Exception as e:
                logger.warning(f"Skipping invalid record: {e}")
                continue
        
        if bulk_create and instances:
            created_instances = model_class.objects.bulk_create(instances, ignore_conflicts=True)
            logger.info(f"Bulk created {len(created_instances)} {model_class.__name__} instances")
            return created_instances
        elif instances:
            created_instances = []
            for instance in instances:
                try:
                    instance.save()
                    created_instances.append(instance)
                except Exception as e:
                    logger.warning(f"Failed to save instance: {e}")
                    continue
            logger.info(f"Created {len(created_instances)} {model_class.__name__} instances")
            return created_instances
        
        return []

    def generate_and_create(self, model_class: models.Model, count: int = 10,
                           exclude_fields: Optional[List[str]] = None,
                           bulk_create: bool = True, 
                           related_objects_cache: Optional[Dict] = None) -> List[models.Model]:
        """
        One-step function to generate mock data and create model instances
        
        Args:
            model_class: Django model class
            count: Number of records to generate
            exclude_fields: List of field names to exclude
            bulk_create: Whether to use bulk_create for better performance
            related_objects_cache: Cache of related objects to avoid repeated queries
            
        Returns:
            List of created model instances
        """
        mock_data = self.generate_mock_data(model_class, count, exclude_fields)
        return self.create_model_instances(model_class, mock_data, bulk_create, related_objects_cache)

    def generate_related_data_set(self, model_relationships: List[Dict[str, Any]], 
                                 shared_cache: bool = True) -> Dict[str, List[models.Model]]:
        """
        Generate related data for multiple models in proper order
        
        Args:
            model_relationships: List of dicts with model info:
                [
                    {'model': Stores, 'count': 10, 'exclude': ['deleted_at']},
                    {'model': StoreSocial, 'count': 20, 'exclude': ['deleted_at']}
                ]
            shared_cache: Whether to share object cache between models
            
        Returns:
            Dictionary mapping model names to created instances
        """
        results = {}
        cache = {} if shared_cache else None
        
        for relationship in model_relationships:
            model_class = relationship['model']
            count = relationship.get('count', 10)
            exclude_fields = relationship.get('exclude', [])
            
            logger.info(f"Generating {count} records for {model_class.__name__}")
            
            instances = self.generate_and_create(
                model_class=model_class,
                count=count,
                exclude_fields=exclude_fields,
                related_objects_cache=cache
            )
            
            results[model_class.__name__] = instances
            
            # Update cache with newly created objects
            if shared_cache and cache is not None:
                cache[model_class.__name__] = instances
                
        return results

    def ensure_related_data_consistency(self, model_class: models.Model, 
                                      related_field_name: str, 
                                      related_values: List[Any]) -> List[Dict[str, Any]]:
        """
        Generate mock data that ensures specific values for foreign key fields
        
        Args:
            model_class: Django model class
            related_field_name: Name of the foreign key field
            related_values: List of related object instances or IDs
            
        Returns:
            List of mock data with consistent foreign key values
        """
        base_schema = self.generate_schema_for_model(model_class)
        
        # Remove the related field from schema since we'll set it manually
        schema = [field for field in base_schema if field['name'] != related_field_name]
        
        # Generate base mock data
        mock_data = self.generate_mock_data(
            model_class=model_class, 
            count=len(related_values),
            custom_schema=schema
        )
        
        # Assign specific related values
        for i, data in enumerate(mock_data):
            if i < len(related_values):
                data[related_field_name] = related_values[i]
                
        return mock_data


# Usage example:
"""
# Example usage in Django management command or script

from your_app.models import Stores, StoreSocial

# Initialize the generator with your Mockaroo API key
generator = MockarooDataGenerator(api_key='your_mockaroo_api_key_here')

# Generate and create 50 Store instances
stores = generator.generate_and_create(
    model_class=Stores,
    count=50,
    exclude_fields=['deleted_at']  # Exclude soft delete field
)

# Generate mock data for StoreSocial (requires existing Stores)
store_social_data = generator.generate_mock_data(
    model_class=StoreSocial,
    count=30,
    exclude_fields=['deleted_at']
)

# Custom schema example for more control
custom_schema = [
    {'name': 'store_cnpj', 'type': 'Regular Expression', 'value': r'\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}'},
    {'name': 'name', 'type': 'Company Name'},
    {'name': 'email', 'type': 'Email Address'},
    {'name': 'status', 'type': 'Boolean'}
]

custom_data = generator.generate_mock_data(
    model_class=Stores,
    count=20,
    custom_schema=custom_schema
)
"""