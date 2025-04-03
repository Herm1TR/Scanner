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
