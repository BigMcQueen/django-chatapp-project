from django.db import models

# Create your models here.
class Chat(models.Model):
    message = models.TextField()
    poster = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='', null=True, blank=True)
    good = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message