from airflow.operators.python import PythonOperator
from airflow.utils.context import Context
from typing import Any, Callable
import logging
from config.settings import APP_SETTINGS

class BaseAppOperator(PythonOperator):
    """Base operator for all app-specific operators"""
    
    def __init__(self, app_name: str, *args, **kwargs):
        self.app_name = app_name
        super().__init__(*args, **kwargs)
        
    def execute(self, context: Context) -> Any:
        """Enhanced execute with app-specific logging and configuration"""
        logger = logging.getLogger(f'{self.app_name}.{self.task_id}')
        
        # Get app-specific settings
        app_config = APP_SETTINGS.get(self.app_name, {})
        
        # Add app context to kwargs
        if hasattr(self, 'python_callable'):
            original_callable = self.python_callable
            
            def wrapped_callable(*args, **kwargs):
                kwargs['app_config'] = app_config
                kwargs['app_logger'] = logger
                return original_callable(*args, **kwargs)
            
            self.python_callable = wrapped_callable
            
        return super().execute(context)