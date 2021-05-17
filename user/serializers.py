from rest_framework import serializers
from .models import User, AdvisorBooking
from advisor.models import Advisor
from advisor.serializers import AdvisorSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class AdvisorBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvisorBooking
        fields = "__all__"
        extra_kwargs = {'user': {'required': False},
                        'advisor': {'required': False}}

    def create(self, validated_data):

        user = validated_data.pop('user')
        user = User.objects.get(id=user)
        advisor = validated_data.pop('advisor')
        advisor = Advisor.objects.get(name=advisor)
        advisor_booking = AdvisorBooking.objects.create(user=user,
                                                        advisor=advisor, **validated_data)
        return advisor_booking


class DetailedBookingSerializer(serializers.ModelSerializer):
    advisor = AdvisorSerializer()

    class Meta:
        model = AdvisorBooking
        fields = ['advisor', 'id', 'booking_time']
