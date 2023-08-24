from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from main1 import EmailMarketingAssistant
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()

# Define request model
class EmailRequest(BaseModel):
    business_type: str
    campaign_goal: str
    product_name: str = None
    product_description: str = None
    user_name: str = None
    post_title: str = None 
    topic: str = None
    website_url: str = None

@app.get("/")
def generate_email(request: EmailRequest):
    logger.info(request.dict())
    assistant = EmailMarketingAssistant()
    
    details = {
        'product_name': request.product_name,
        'product_description': request.product_description,
        'user_name': request.user_name,
        'post_title': request.post_title,
        'topic': request.topic
    }

    if request.website_url:
        company_description = assistant.get_company_description(request.website_url)

    email_contents = assistant.get_sample_email(request.business_type, request.campaign_goal, **details)

    return {"emails": email_contents, "company_description": company_description if request.website_url else None}

