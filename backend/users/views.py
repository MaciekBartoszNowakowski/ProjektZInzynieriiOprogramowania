from django.shortcuts import render
from django.http import JsonResponse

def hello_world_view(request):
    data = {
        "message": "Hello from Django!",
        "status": "success",
        "data": {
            "greeting": "Hello, World!"
        }
    }

    return JsonResponse(data)