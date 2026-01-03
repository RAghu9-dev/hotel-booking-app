from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.utils.text import slugify
from accounts.models import Hotel

def send_test_email(email, token):

    subject = 'Email Verification for OYO'
    message = f"""Hi, Please verify your email address by clicking the below link...

        http://127.0.0.1:8000/accounts/verify-account/{token}
    
    """
    send_mail(
        subject,
        message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

def generateToken():
    token = str(uuid.uuid4())
    return token

def send_email_with_otp(email, otp):
    subject = 'OTP for account login in OYO_CLONE'
    message = f"""Hi, Here is your OTP for login 

        {otp}
    
    """
    send_mail(
        subject,
        message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )


def generate_slug(hotel_name):
    slug = slugify(hotel_name) + "-" + str(uuid.uuid4()).split("-")[0]
    if Hotel.objects.filter(hotel_slug = slug).exists():
        return generate_slug(hotel_name)

    return slug
    


