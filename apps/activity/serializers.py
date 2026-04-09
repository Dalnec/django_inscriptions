from rest_framework import serializers
from .models import Activity, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug", "color"]
        read_only_fields = ["id", "slug"]


class NestedTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug", "color"]
        extra_kwargs = {
            "name": {"validators": []},
            "slug": {"validators": []},
        }

class ActivitySerializer(serializers.ModelSerializer):
    tags = NestedTagSerializer(many=True, required=False)

    class Meta:
        model = Activity
        fields = "__all__"

    def to_internal_value(self, data):
        import json
        
        # DRF expects normal python objects if it's not a QueryDict.
        # QueryDicts trigger html.parse_html_list to look for tags[0]name rather than tags
        if hasattr(data, 'lists'):
            parsed_data = {}
            for key, value in data.lists():
                # For basic fields, just take the first item if there is only 1.
                # Multi-item arrays will survive as lists.
                if len(value) == 1:
                    parsed_data[key] = value[0]
                else:
                    parsed_data[key] = value
        else:
            if hasattr(data, 'copy'):
                parsed_data = data.copy()
            else:
                parsed_data = dict(data)
                
        # Now parse tags and other JSON encoded fields
        for field in ["tags", "settings", "location"]:
            field_val = parsed_data.get(field)
            if isinstance(field_val, str):
                try:
                    parsed_data[field] = json.loads(field_val)
                except json.JSONDecodeError:
                    pass
                    
        return super().to_internal_value(parsed_data)

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