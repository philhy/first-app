from django.db import models
from django.contrib.auth.models import User

class Prediction(models.Model):
    CATEGORIES = [
        (0, 'Sports')
    ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')

    def __str__(self):
        return self.title