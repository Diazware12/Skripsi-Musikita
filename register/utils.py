from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from six import text_type #install six dulu

class AppTokenGenerator (PasswordResetTokenGenerator):
    
    def makeHashvalue (self, user, timestamp): 
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))

token_generator = AppTokenGenerator ()