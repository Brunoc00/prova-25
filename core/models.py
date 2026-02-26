from django.db import models
from django.utils import timezone
import uuid


class BaseModel(models.Model):
    """
    Modelo base abstrato com campos comuns
    Todos os modelos devem herdar deste para padronização
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['is_active']),
        ]

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id}>"


class User(BaseModel):
    name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)

    class Meta(BaseModel.Meta):
        ordering = ["name"]
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name


class Tag(BaseModel):
    """Modelo para tags/categorias de tarefas"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Task(BaseModel):
    """Modelo para tarefas"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.IntegerField(default=0)  # 0 = baixa, 1 = média, 2 = alta
    tags = models.ManyToManyField(Tag, through='TaskTag', blank=True)
    due_date = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['priority', '-created_at']),
        ]

    def __str__(self):
        return self.title


class TaskTag(BaseModel):
    """Modelo de relacionamento Many-to-Many entre Task e Tag"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('task', 'tag')
        verbose_name_plural = 'Task Tags'
        indexes = [
            models.Index(fields=['task', 'tag']),
        ]

    def __str__(self):
        return f"{self.task.title} - {self.tag.name}"



