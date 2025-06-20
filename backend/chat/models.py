import random
import string
import os
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


def generate_uid():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))


class Chat(models.Model):
    uid = models.CharField(max_length=12, unique=True, default=generate_uid, db_index=True)
    headline = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats', null=True)
    is_shared = models.BooleanField(default=False)
    system_prompt = models.TextField(blank=True, default='')
    tools = models.JSONField(default=list, blank=True)  # List of tool names or IDs

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.headline} ({self.uid})"


class Prompt(models.Model):
    STATUS_CHOICES = [
        ('queued', 'Queued'),
        ('running', 'Running'),
        ('finished', 'Finished'),
    ]

    RESULT_CHOICES = [
        ('success', 'Success'),
        ('failure', 'Failure'),
    ]

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='prompts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='queued')
    result = models.CharField(max_length=10, choices=RESULT_CHOICES, null=True, blank=True)
    input_text = models.TextField()
    output_text = models.TextField(blank=True, default='')
    llm_messages = models.JSONField(default=list, blank=True)
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)
    files = models.ManyToManyField('File', blank=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"[{self.chat.uid}] {self.input_text:.30}..."


def upload_to(instance, filename):
    """Generate upload path: <year>/<month>/<random6chars>/<original_filename>"""
    now = timezone.now()
    random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{now.year}/{now.month:02d}/{random_chars}/{filename}"


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to=upload_to)
    media_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{os.path.basename(self.file.name)} ({self.user.username})"
