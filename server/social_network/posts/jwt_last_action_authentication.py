from datetime import datetime

from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTLastActionAuthentication(JWTAuthentication):

    def get_user(self, validated_token):
        """change last_action of user to current time if auth succeeded."""
        user = super().get_user(validated_token)
        user.last_action = datetime.now()
        user.save()
        return user
