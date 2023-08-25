from django.urls import path
from email_app.views import generate_emails

urlpatterns = [
    path('', generate_emails, name='generate-emails'),
]
