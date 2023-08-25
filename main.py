import openai
from bs4 import BeautifulSoup
import requests
from fastapi import FastAPI, Body


app = FastAPI()
# Make sure you set up your API key
openai.api_key = 'lol'



class EmailMarketingAssistant:

    SAMPLE_EMAILS = {
        'e-commerce': {
            'convince_to_buy': [
                "Introducing our new {product_name}: {product_description}. Grab yours now!",
                "Experience the best with our new {product_name}. {product_description}. Limited stock!",
                "Why wait? The {product_name} you've always wanted is here. {product_description}."
            ]
        },
        'people': {
            'welcome_new_user': [
                "Welcome {user_name}! We're thrilled to have you on board.",
                "Hi {user_name}, thanks for choosing us! Let's embark on this journey together.",
                "A warm welcome to our community, {user_name}!"
            ],
        },
        'blog': {
            'new_blog': [
                "Just out: our new blog post, {post_title}, covering everything about {topic}. Dive in!",
                "Unveiling our latest piece: {post_title}. Discover more about {topic}.",
                "{post_title} - a fresh take on {topic}. Read now!"
            ]
        }
    }

    def get_sample_email(self, business_type, campaign_goal, **details):
        sample_emails = self.SAMPLE_EMAILS.get(business_type, {}).get(campaign_goal, [])
        if not sample_emails:
            return ["Sorry, no sample email found for your criteria."] * 5
        
        refined_emails = []
        for sample in sample_emails:
            refined_emails.append(self.refine_prompt(sample.format(**details)))

        return refined_emails

    def refine_prompt(self, prompt):
        gpt3_message = {
            "messages": [{
                "role": "user",
                "content": f"Given this sample email: '{prompt}', create a similar yet unique marketing email."
            }]
        }
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=gpt3_message['messages'],
            max_tokens=200,
        )
        return response.choices[0].message['content'].strip()

    def get_company_description(self, website_url):
        try:
            response = requests.get(website_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            description = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
            if description:
                return description.get('content')
            else:
                return "Description not found. Please provide manually."
        except Exception as e:
            return f"Error fetching description: {e}"

assistant = EmailMarketingAssistant()

@app.post("/generate-email/")
async def generate_email(
    business_type: str = Body(..., embed=True),
    campaign_goal: str = Body(..., embed=True),
    product_name: str = Body(None, embed=True),
    product_description: str = Body(None, embed=True),
    user_name: str = Body(None, embed=True),
    post_title: str = Body(None, embed=True),
    topic: str = Body(None, embed=True),
    website_url: str = Body(None, embed=True)
):

    details = {
        'product_name': product_name,
        'product_description': product_description,
        'user_name': user_name,
        'post_title': post_title,
        'topic': topic
    }

    if website_url:
        company_description = assistant.get_company_description(website_url)
        details['company_description'] = company_description

    email_contents = assistant.get_sample_email(business_type, campaign_goal, **details)
    return {"Recommended Email Contents": email_contents}
