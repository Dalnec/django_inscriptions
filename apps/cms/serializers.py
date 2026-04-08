from rest_framework import serializers

from .models import MediaAsset, PageContent


class MediaAssetSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = MediaAsset
        fields = ["id", "file", "original_filename", "url"]
        read_only_fields = ["id"]

    def get_url(self, obj):
        if obj.file:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class MediaAssetUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaAsset
        fields = ["id", "activity", "file", "original_filename"]
        read_only_fields = ["id"]


class PageContentSerializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField()

    class Meta:
        model = PageContent
        fields = "__all__"

    def get_media(self, obj):
        assets = obj.activity.cms_media_assets.all()
        return MediaAssetSerializer(assets, many=True, context=self.context).data

    def to_representation(self, instance):
        def get_image_url(image_field):
            if image_field:
                request = self.context.get("request")
                if request:
                    return request.build_absolute_uri(image_field.url)
                return image_field.url
            return None

        return {
            "page_config": {
                "title": instance.page_title,
                "theme_color": instance.theme_color,
                "language": instance.language,
            },
            "hero": {
                "motto": instance.hero_motto,
                "verse": instance.hero_verse,
                "citation": instance.hero_citation,
                "date_label": instance.hero_date_label,
                "background_image": get_image_url(instance.hero_background_image),
            },
            "vision_section": {
                "title": instance.vision_title,
                "description": instance.vision_description,
                "features": [
                    {
                        "icon": instance.vision_feature_1_icon,
                        "label": instance.vision_feature_1_label,
                    },
                    {
                        "icon": instance.vision_feature_2_icon,
                        "label": instance.vision_feature_2_label,
                    },
                ],
                "images": [
                    get_image_url(instance.vision_image_1),
                    get_image_url(instance.vision_image_2),
                ],
            },
            "pricing_plans": {
                "section_title": instance.pricing_section_title,
                "currency": instance.pricing_currency,
                "plans": [
                    {
                        "id": instance.plan_1_id,
                        "name": instance.plan_1_name,
                        "price": float(instance.plan_1_price),
                        "original_price": float(instance.plan_1_original_price),
                        "subtitle": instance.plan_1_subtitle,
                        "is_recommended": instance.plan_1_is_recommended,
                        "cta_text": instance.plan_1_cta_text,
                        "benefits": instance.plan_1_benefits,
                    },
                    {
                        "id": instance.plan_2_id,
                        "name": instance.plan_2_name,
                        "price": float(instance.plan_2_price),
                        "original_price": float(instance.plan_2_original_price),
                        "subtitle": instance.plan_2_subtitle,
                        "is_recommended": instance.plan_2_is_recommended,
                        "cta_text": instance.plan_2_cta_text,
                        "whatsapp_link": instance.plan_2_whatsapp_link,
                        "benefits": instance.plan_2_benefits,
                    },
                ],
            },
            "location": {
                "place_name": instance.location_place_name,
                "address": instance.location_address,
                "city": instance.location_city,
                "description": instance.location_description,
                "map_url": instance.location_map_url,
                "amenities": instance.location_amenities,
            },
            "footer": {
                "cta_title": instance.footer_cta_title,
                "organization": instance.footer_organization,
                "year": instance.footer_year,
            },
        }


class PageContentCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageContent
        fields = [
            "page_title",
            "theme_color",
            "language",
            "hero_motto",
            "hero_verse",
            "hero_citation",
            "hero_date_label",
            "hero_background_image",
            "vision_title",
            "vision_description",
            "vision_feature_1_icon",
            "vision_feature_1_label",
            "vision_feature_2_icon",
            "vision_feature_2_label",
            "vision_image_1",
            "vision_image_2",
            "pricing_section_title",
            "pricing_currency",
            "plan_1_id",
            "plan_1_name",
            "plan_1_price",
            "plan_1_original_price",
            "plan_1_subtitle",
            "plan_1_is_recommended",
            "plan_1_cta_text",
            "plan_1_benefits",
            "plan_2_id",
            "plan_2_name",
            "plan_2_price",
            "plan_2_original_price",
            "plan_2_subtitle",
            "plan_2_is_recommended",
            "plan_2_cta_text",
            "plan_2_whatsapp_link",
            "plan_2_benefits",
            "location_place_name",
            "location_address",
            "location_city",
            "location_description",
            "location_map_url",
            "location_amenities",
            "footer_cta_title",
            "footer_organization",
            "footer_year",
        ]
