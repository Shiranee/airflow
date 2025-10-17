"""
Django command to wait for Redis to be available.
"""
import time
from django.core.management.base import BaseCommand
from django.conf import settings
from django_redis import get_redis_connection
from redis.exceptions import ConnectionError

class Command(BaseCommand):
    """Django command to wait for Redis to be available."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Waiting for Redis...')
        max_retries = 20
        retry_delay = 1  # seconds
        
        for i in range(max_retries):
            try:
                # Use the same connection method as your cache configuration
                conn = get_redis_connection("default")
                print(conn)
                conn.ping()
                self.stdout.write(self.style.SUCCESS('Redis is available!'))
                return
            except ConnectionError as e:
                if i == max_retries - 1:
                    self.stdout.write(self.style.ERROR('Could not connect to Redis'))
                    raise ConnectionError(f'Could not connect to Redis after {max_retries} attempts: {str(e)}')
                
                self.stdout.write(f'Attempt {i + 1}/{max_retries}: Redis unavailable, waiting {retry_delay} second...')
                time.sleep(retry_delay)
