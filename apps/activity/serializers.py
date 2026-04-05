from rest_framework import serializers
from .models import Activity, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug", "color"]
        read_only_fields = ["id", "slug"]


class ActivitySerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Activity
        fields = "__all__"

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        activity = Activity.objects.create(**validated_data)
        self._handle_tags(activity, tags_data)
        return activity

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", None)
        instance = super().update(instance, validated_data)
        if tags_data is not None:
            instance.tags.clear()
            self._handle_tags(instance, tags_data)
        return instance

    def _handle_tags(self, activity, tags_data):
        for tag_data in tags_data:
            tag_name = tag_data.get("name")
            if tag_name:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                activity.tags.add(tag)