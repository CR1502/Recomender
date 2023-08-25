import openai
from bs4 import BeautifulSoup
import requests

# Make sure you set up your API key
<<<<<<< HEAD
openai.api_key = ''
=======
openai.api_key = 'sk-'
>>>>>>> 59424926c8bba657763d7644b1418b553655b6b4


class EmailMarketingAssistant:

    TEMPLATES = {
        'e-commerce': {
            'convince_to_buy': "Convince customers to buy the new product named {product_name}. Description: {product_description}."
        },
        'people': {
            'welcome_new_user': "Welcome a new user {user_name} to our platform after purchasing a {product} from our company.",
        },
        'blog': {
            'new_blog': "Introduce a new blog post titled {post_title} about {topic}."
        }
    }

    def refine_prompt(self, prompt):
        response = openai.Completion.create(
            model="davinci",
            prompt=f"Optimize this prompt for generating marketing content: {prompt}",
            max_tokens=200,
            n=1,
            temperature=0.5
        )
        return response.choices[0].text.strip()

    def get_email_template(self, business_type, campaign_goal, **details):
        prompt = self.TEMPLATES.get(business_type, {}).get(campaign_goal, "")
        if not prompt:
            return ["Sorry, no template found for your criteria."] * 5

        # Refine the prompt using davinci
        optimized_prompt = self.refine_prompt(prompt.format(**details))

        # Formulate the message for GPT-3.5-turbo using the optimized prompt
        gpt3_message = {
            "messages": [{
                "role": "system",
                "content": f"Given that we need to {optimized_prompt}, please provide 5 different marketing email content suggestions:"
            }]
        }

        # Query GPT-3.5-turbo using the chat endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=gpt3_message['messages']
        )

        # Extract the email content suggestions from the response
        email_contents = response.choices[0].message['content'].split('\n')[:5] # Assuming the model returns emails separated by newlines.

        return [content.strip() for content in email_contents]

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

if __name__ == "__main__":
    assistant = EmailMarketingAssistant()

    business_type = input("Enter your business type (e-commerce, people, blog, etc.): ")
    campaign_goal = input("Enter your campaign goal (convince_to_buy, welcome_new_user, new_blog): ")

    details = {}
    
    # For e-commerce related prompts
    if business_type == "e-commerce":
        details['product_name'] = input("Enter the product name: ")
        if campaign_goal in ['convince_to_buy']:
            details['product_description'] = input("Provide a brief description of the product: ")
    
    # For new cutomer related prompts
    if business_type == "people" and campaign_goal in ['welcome_new_user']:
        details['user_name'] = input("Provide new users name: ")
        details['product'] = input('Provide product name: ')

    # For blog related prompts
    elif business_type == "blog" and campaign_goal == "new_blog":
        details['post_title'] = input("Enter the blog post title: ")
        details['topic'] = input("Enter the post topic: ")

    # Fetch company website details
    website_url = input("Enter your company website URL (or press Enter to skip): ")
    if website_url:
        company_description = assistant.get_company_description(website_url)
        print(f"Fetched company description: {company_description}")

    # Now you can use this `company_description` variable in your chat model or anywhere else as needed
    email_contents = assistant.get_email_template(business_type, campaign_goal, **details)
    print("\nRecommended Email Contents:\n")
    for i, content in enumerate(email_contents, 1):
        print(f"Email {i}:\n{content}\n")
