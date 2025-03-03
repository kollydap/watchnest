from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from ipware import get_client_ip

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    device = serializers.CharField(max_length=250, required=True)

    def validate_email(self, value):
        """Ensure email is unique"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get("first_name")
        user.last_name = self.validated_data.get("last_name")
        user.device = self.validated_data.get("device")
        client_ip, is_routable = get_client_ip(request)

        user.registration_ip = client_ip
        user.save()





class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "pk",
            "username",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "gender",
            "date_of_birth",
            "is_email_verified",
            "is_phone_verified",
            "profile_picture",
            "last_purchase_date",
            "online_status",
            "account_status",
        ]

