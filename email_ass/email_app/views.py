from django.shortcuts import render
from django.http import JsonResponse
# Import your EmailMarketingAssistant class here
from email_app.main1 import EmailMarketingAssistant

def generate_emails(request):
    email_contents = []
    if request.method == 'POST':
        # Get data from the form
        mail_type = request.POST.get('mail_type')
        campaign_goal = request.POST.get('campaign_goal')
        details = {
            'product_name': request.POST.get('product_name'),
            'product_description': request.POST.get('product_description'),
            'user_name': request.POST.get('user_name'),
            'post_title': request.POST.get('post_title'),
            'topic': request.POST.get('topic')
        }

        # Process data using the EmailMarketingAssistant class
        assistant = EmailMarketingAssistant()
        email_contents = assistant.get_sample_email(mail_type, campaign_goal, **details)


    return render(request, 'form.html', {'emails': email_contents})
