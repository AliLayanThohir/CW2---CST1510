#Import needed for AI
from openai import OpenAI

#Class to wrap around OpenAI API for domain-specific assistance
class AIAssistant:
    """Ai Assistant to help with domain."""
    
    #Constructor method to initialize the assistant with API key and Role
    def __init__(self, api_key, role="General"):
        self.client = OpenAI(api_key=api_key)
        self.role = role
        
        #Prompts for different roles in the domain
        self.prompts = {
            "Cybersecurity Analyst": """You are a Cybersecurity Expert Assistant.
            - Analyze incidents, threats, and logs.
            - Provide technical guidance on malware, phishing, and DDoS.
            - Use standard terminology (MITRE ATT&CK, CVE).
            - Prioritize actionable mitigation steps.""",
            
            "Data Scientist": """You are a Data Science Expert Assistant.
            - Assist with data cleaning, preprocessing, and metadata management.
            - Provide Python pandas code for data manipulation.
            - Explain statistical concepts and data visualization techniques.
            - Help organize and classify datasets.""",
            
            "IT Administrator": """You are an IT Operations Expert Assistant.
            - Assist with IT ticket management and prioritization.
            - Provide solutions for common hardware, software, and network issues.
            - Suggest workflows for resolving support tickets efficiently.
            - Use a professional, service-oriented tone.""",
            
            "General": """You are a helpful assistant for the Multi-Domain Intelligence Platform.
            - Assist users with general navigation and platform usage.
            - Answer questions clearly and professionally."""
        }
        
        #Select the appropriate prompt based on the user's role, default to General if not found
        self.current_prompt = self.prompts.get(role, self.prompts["General"])
        
        #List to store conversation history, initialized with the system prompt
        self.history = [
            {
                "role": "system",
                "content": self.current_prompt
            }
        ]

    #Function to add user message to history
    def add_user_message(self, message):
        self.history.append({"role": "user", "content": message})

    #Function to get response from OpenAI
    def get_response(self):
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.history
        )
        response = completion.choices[0].message.content
        #Add assistant response to history
        self.history.append({"role": "assistant", "content": response})
        return response
    
    #Function to clear conversation history
    def clear_history(self):
        #Resets history but keeps the role-specific system prompt
        self.history = [self.history[0]]