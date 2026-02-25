from rest_framework import serializers
from core.models import Task, Tag, TaskTag, User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_active']


class TagSerializer(serializers.ModelSerializer):
    """Serializer padrão para Tag (leitura/GET)"""
    class Meta:
        model = Tag
        fields = ['id', 'name', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class TaskTagSerializer(serializers.ModelSerializer):
    """Serializer padrão para TaskTag (leitura/GET)"""
    tag_detail = TagSerializer(source='tag', read_only=True)

    class Meta:
        model = TaskTag
        fields = ['id', 'tag', 'tag_detail', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class TaskDetailSerializer(serializers.ModelSerializer):
    """Serializer padrão para Task com tags aninhadas (leitura/GET)"""
    tags = TagSerializer(many=True, read_only=True)
    tag_list = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority',
                  'tags', 'tag_list', 'is_active', 'created_at', 'updated_at',
                  'due_date', 'completed_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'completed_at']

    def get_tag_list(self, obj):
        """Retorna IDs das tags"""
        return list(obj.tags.values_list('id', flat=True))