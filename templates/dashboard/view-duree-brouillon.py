# views.py
from datetime import timedelta

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@require_POST
@csrf_exempt
def update_duration(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    duration = request.POST.get("duration")
    todo.duration = timedelta(seconds=int(duration))
    todo.save()
    return JsonResponse({"status": "success"})
