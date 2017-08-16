from rest_framework import serializers
import datetime


class AddTopSellerSerializer(serializers.Serializer):
    category = serializers.CharField()
    start_time = serializers.DateField(allow_null=True)
    end_time = serializers.DateField(allow_null=True)

    def validate(self, obj):
        if obj['start_time'] is None:
            obj['start_time'] = datetime.datetime.now().date()
        if obj['end_time'] is None:
            obj['end_time'] = obj['start_time'] + datetime.timedelta(weeks=4)
        return obj
