from rest_framework import serializers
from .models import Advisor

class AdvisorSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length = None, use_url = True)
    class Meta:
        model = Advisor
        fields = '__all__'
