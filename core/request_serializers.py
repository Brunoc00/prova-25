from rest_framework import serializers
from core.models import Task, Tag


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer customizado para criar/atualizar tarefas com tags múltiplas
    Usado apenas para POST, PUT e PATCH
    """
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority',
                  'tag_ids', 'is_active', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        """Criar tarefa e adicionar tags"""
        tags = validated_data.pop('tag_ids', [])
        task = Task.objects.create(**validated_data)

        # Adicionar tags à tarefa
        for tag in tags:
            from core.models import TaskTag
            TaskTag.objects.create(task=task, tag=tag)

        return task

    def update(self, instance, validated_data):
        """Atualizar tarefa e tags"""
        tags = validated_data.pop('tag_ids', None)

        # Atualizar campos da tarefa
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Se tags foram fornecidas, atualizar
        if tags is not None:
            # Remover tags antigas
            instance.taskTag_set.all().delete()
            # Adicionar novas tags
            from core.models import TaskTag
            for tag in tags:
                TaskTag.objects.create(task=instance, tag=tag)

        return instance