from rest_framework import serializers
from ..models import Categories


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Categories
        fields = [
            "id",
            "name",
            "slug",
            "parent",
            "children",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_children(self, obj):
        children_qs = obj.children.filter(is_active=True)
        return CategorySerializer(children_qs, many=True).data
