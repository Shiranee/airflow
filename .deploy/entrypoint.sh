#!/bin/sh
set -e

echo "🐍 entrypoint.sh: [$(whoami)] [Python $(python --version)]"
echo "🚀 Django App with Celery starting..."

cd $DJANGO_PATH/app
echo "⏳ Waiting for database and redis..."
python manage.py wait_for_db
python manage.py wait_for_redis

echo "🎬 Starting supervisord"
supervisord -c $DJANGO_PATH/.develop/config/supervisor.conf