from rest_framework import serializers

class SeedSerializer(serializers.Serializer):
    post = serializers.CharField(max_length=100)
    class Meta:
        filds = ['post',]