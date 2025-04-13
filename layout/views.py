from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Box, OperationLog
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .serializers import BoxSerializer, OperationLogSerializer
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import random

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            default_colors = ["#FF0000", "#00FF00", "#0000FF", "#FFA500", "#800080"]
            color = random.choice(default_colors)
            # create default Box
            Box.objects.create(
                x=50,
                y=50,
                width=100,
                height=100,
                owner=user,
                color=color
            )
            return redirect('floorplan')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def floorplan_view(request):
    """
    Renders the page with the floor plan background and a draggable/resizable box for a login user.
    """
    boxes = Box.objects.filter(owner=request.user)
    allowed_advanced_actions = request.user.groups.filter(name__in=["Engineer", "Admin"]).exists()
    return render(request, 'layout/floorplan.html', {
        'boxes': boxes,
        'allowed_advanced_actions': allowed_advanced_actions,
    })

@csrf_exempt
@login_required
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

            # retrieve the box and verify the user is the owner before updating its properties
            box = Box.objects.get(pk=box_id)
            if box.owner != request.user:
                return JsonResponse({'status': 'error', 'message': 'Permission denied.'}, status=403)
            
            box.x = x
            box.y = y
            box.width = width
            box.height = height
            box.save()
            
            # create operation log
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

class IsOwner(permissions.BasePermission):
    """
    Allow access only to the owner
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class BoxViewSet(viewsets.ModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Return only Boxes belonging to the current user
        return Box.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically set the owner to the currently logged-in user
        serializer.save(owner=self.request.user)

class OperationLogViewSet(viewsets.ModelViewSet):
    queryset = OperationLog.objects.all()
    serializer_class = OperationLogSerializer

    def get_queryset(self):
        # Return only Operationlog belonging to the current user
        return OperationLog.objects.filter(box__owner=self.request.user).order_by('-timestamp')