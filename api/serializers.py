from rest_framework import serializers
from api.models import User, Schedule

'''File to serialize all the models and their attributes,
that way, they can be transformed into tables for the database
'''

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'