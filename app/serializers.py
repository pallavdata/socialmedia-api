from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from .models import User_access
import re

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    username = serializers.CharField(validators=[])
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    email = serializers.EmailField(validators=[])

    class Meta:
        model = User_access
        fields = ['username', 'email', 'password', 'password2','first_name','last_name']
        extra_kwargs = {
            'username': {'min_length': 5, 'max_length': 10},
            'password': {'min_length': 8, 'max_length': 20},
            'password2': {'min_length': 8, 'max_length': 20},
        }
    def validate(self, data):
        data = super().validate(data)
        password = data['password']
        pass2 = data['password2']
        username = data.get('username')
        email = data.get('email')
        errors = {}

        pattern = re.compile('[A-Z]')
        pattern2 = re.compile('[a-z]')
        pattern3 = re.compile('[0-9]')
        pattern4 = re.compile('[!@#$%^&*(),.?":{}|<>]')

        if not pattern.search(password) or not pattern2.search(password) or not pattern3.search(password) or not pattern4.search(password):
                list = ['should contain at least one upper case','should contain at least one lower case','should contain at least one digit','should contain at least one Special character']
                errors['password'] = list

        else:
            if password != pass2:
                error_message = 'Password did not matched. Enter the same password as above'
                field = 'password2'
                errors[field] = [error_message]

        try:
            user_name = User_access.objects.get(username=username)
            errors["username"] = [f"Username {username} is already in use."]
        except User_access.DoesNotExist:
            pass

        try:
            user_name = User_access.objects.get(email=email)
            errors["email"] = [f"Email {email} is already in use."]
        except User_access.DoesNotExist:
            pass

        if errors:
            raise serializers.ValidationError(errors)
        return data

    def create(self, validated_data):
        password = validated_data.pop('password2')
        user = User_access(**validated_data)
        user.set_password(password)
        user.save()
        return user
