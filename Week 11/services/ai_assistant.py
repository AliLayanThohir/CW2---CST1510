#Import needed for AI
from openai import OpenAI

#Class to use AI assistant for help.
class AIAssistant:
    """Handles AI assistant interactions."""
    
    #Constructor to initialize the assistant with API key
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        #List to store conversation history
        self.history = [
            {
                "role": "system",
                "content": """You are a cybersecurity expert assistant.
                - Analyze incidents and threats
                - Provide technical guidance
                - Explain attack vectors and mitigations
                - Use standard terminology (MITRE ATT&CK, CVE)
                - Prioritize actionable recommendations
                Tone: Professional, technical
                Format: Clear, structured responses"""
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
        self.history = [self.history[0]] 