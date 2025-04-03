from django.db import models


class Box(models.Model):
    """
    Stores x/y coordinates and width/height for each 'square' or 'box'.
    """
    x = models.FloatField(default=0.0)      # top-left X coordinate
    y = models.FloatField(default=0.0)      # top-left Y coordinate
    width = models.FloatField(default=100.0)
    height = models.FloatField(default=100.0)

    def __str__(self):
        return f"Box({self.id}) - x:{self.x}, y:{self.y}, w:{self.width}, h:{self.height}"

class OperationLog(models.Model):
    ACTION_CHOICES = (
        ('drag', '拖曳'),
        ('resize', '縮放'),
    )
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    x = models.FloatField()
    y = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Box {self.box.id} {self.action} at {self.timestamp}"