from rest_framework import serializers
from wagtail_airtable.serializers import AirtableSerializer


class FeatureDescriptionSerializer(AirtableSerializer):
    """
    FeatureDescription serializer used when importing Airtable records.
    """

    title = serializers.CharField(max_length=255, required=False)
    introduction = serializers.CharField(max_length=255, required=False)
    documentation_link = serializers.CharField(max_length=255, required=False)
