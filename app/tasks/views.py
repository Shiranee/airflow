from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from .tasks import process_user_data, fetch_external_data
from .celery import app as celery_app

@api_view(['POST'])
def start_user_processing(request):
    """Start user data processing task"""
    user_id = request.data.get('user_id')
    if not user_id:
        return Response(
            {'error': 'user_id is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    task = process_user_data.delay(user_id)
    return Response({
        'task_id': task.id,
        'status': 'Task queued',
        'user_id': user_id
    })

@api_view(['GET'])
def get_task_status(request, task_id):
    """Get task status"""
    result = AsyncResult(task_id, app=celery_app)
    
    response_data = {
        'task_id': task_id,
        'status': result.status,
        'result': result.result if result.ready() else None
    }
    
    if result.failed():
        response_data['error'] = str(result.result)
    
    return Response(response_data)

@api_view(['POST'])
def fetch_data_async(request):
    """Fetch external data asynchronously"""
    api_url = request.data.get('api_url')
    if not api_url:
        return Response(
            {'error': 'api_url is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    task = fetch_external_data.delay(api_url)
    return Response({
        'task_id': task.id,
        'status': 'Task queued'
    })