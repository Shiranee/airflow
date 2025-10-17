"""
Test custom Django management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase
from redis.exceptions import ConnectionError as RedisConnectionError


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        patched_check.side_effect = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])

class WaitForRedisCommandTests(SimpleTestCase):
    """Test wait_for_redis command."""

    @patch('redis.Redis.ping')
    def test_wait_for_redis_ready(self, patched_ping):
        """Test waiting for redis if redis ready."""
        patched_ping.return_value = True

        call_command('wait_for_redis')

        patched_ping.assert_called_once()

    @patch('time.sleep')
    @patch('redis.Redis.ping')
    def test_wait_for_redis_delay(self, patched_ping, patched_sleep):
        """Test waiting for redis when getting ConnectionError."""
        patched_ping.side_effect = [RedisConnectionError] * 5 + [True]

        call_command('wait_for_redis')

        self.assertEqual(patched_ping.call_count, 6)
        patched_ping.assert_called_with()