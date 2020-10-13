from rest_framework import serializers
from wagtail_airtable.serializers import AirtableSerializer


class BlogPageSerializer(AirtableSerializer):
    """
    BlogPage serializer used when importing Airtable records.
    """

    title = serializers.CharField(max_length=255, required=True)
    live = serializers.BooleanField()
