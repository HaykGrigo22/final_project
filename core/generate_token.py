from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return f"{user.email}{timestamp}{user.is_active}"


generate_user_token = UserTokenGenerator()
