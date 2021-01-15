from rest_framework import serializers

from .models import Recipe


class FavoriteSerializer(serializers.ModelSerializer):
    success = serializers.SerializerMethodField()

    class Meta:
        fields = ["success"]
        model = Recipe

    def get_success(self, obj):
        return obj.is_favorite
