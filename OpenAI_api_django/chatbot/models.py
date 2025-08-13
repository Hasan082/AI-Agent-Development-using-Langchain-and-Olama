from django.db import models
from pgvector.django import VectorField



class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    embedding = VectorField(dimensions=384, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    
class ChatMessage(models.Model):
    user_id = models.CharField(max_length=255)
    message = models.TextField()
    is_bot = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        sender = "Bot" if self.is_bot else "User"
        return f"{sender} ({self.user_id}): {self.message[:50]}"