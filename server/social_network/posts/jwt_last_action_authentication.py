from datetime import datetime

from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTLastActionAuthentication(JWTAuthentication):

    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        user.last_action = datetime.now()
        user.save()
        return user
