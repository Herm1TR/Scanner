from django.shortcuts import render
from .models import Box, OperationLog
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def floorplan_view(request):
    """
    Renders the page with the floor plan background and draggable/resizable boxes.
    """
    boxes = Box.objects.all()
    return render(request, 'layout/floorplan.html', {'boxes': boxes})

@csrf_exempt
def update_box_view(request):
    """
    Receives updated box data via POST, saves to DB, and returns success/fail.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            box_id = data.get('id')
            x = data.get('x')
            y = data.get('y')
            width = data.get('width')
            height = data.get('height')
            action = data.get('action', 'update')

            box = Box.objects.get(pk=box_id)
            box.x = x
            box.y = y
            box.width = width
            box.height = height
            box.save()
            
            # 記錄操作日誌
            if action in ['drag', 'resize']:
                OperationLog.objects.create(
                    box=box,
                    action=action,
                    x=x,
                    y=y,
                    width=width,
                    height=height
                )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)