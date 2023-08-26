from django.urls import path
# In email_app/urls.py
from email_app.views import generate_emails

urlpatterns = [
    path('', generate_emails, name='generate-emails'),
]

