from rest_framework import serializers
from .models import ProspectiveUser

class ProspectiveUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProspectiveUser
        fields = ('id', 'full_names', 'email', 'phone_number', 'education', 'current_job')
