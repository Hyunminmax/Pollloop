from django.shortcuts import get_object_or_404
from rest_framework import serializers

class InputFileSerializer(serializers.Serializer):
    input_source = serializers.CharField(write_only=True)
    user = serializers.UUIDField(read_only=True, required=False)
    # form = serializers.UUIDField(write_only=True, required=False)
    form_title = serializers.CharField(write_only=True, required=False)
    question_order = serializers.IntegerField(write_only=True, required=False)
    option_number = serializers.IntegerField(write_only=True, required=False)
    file = serializers.FileField(write_only=True)