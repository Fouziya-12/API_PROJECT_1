from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirmation']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        """Ensure passwords match before saving."""
        password = data.get('password')
        password2 = data.get('password_confirmation')

        if password != password2:
            raise serializers.ValidationError({'password_confirmation': 'Passwords do not match.'})
        return data

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error':'Email already exists'})

        account = User(email=self.validated_data['email'],username=self.validated_data['username'])
        acccount.set_password(password)
        account.save()
        return account

    def create(self, validated_data):
        validated_data.pop('password_confirmation')  # Remove before saving
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
