import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ChatbotEngine:

    def __init__(self):

        # Initialize Groq client
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )

        # Default model
        self.model = "llama-3.3-70b-versatile"

        # Chat history
        self.history = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            }
        ]

    # Add few-shot examples
    def add_few_shot_examples(self, examples):

        for user_msg, assistant_msg in examples:

            self.history.append({
                "role": "user",
                "content": user_msg
            })

            self.history.append({
                "role": "assistant",
                "content": assistant_msg
            })

    # Get chat history
    def get_history(self):
        return self.history

    # Clear history
    def clear_history(self):

        self.history = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            }
        ]

    # Append assistant response
    def append_assistant_response(self, response):

        self.history.append({
            "role": "assistant",
            "content": response
        })

    # Chat function
    def chat(self, user_input, use_cot=False, stream=False):

        # Optional Chain-of-Thought
        if use_cot:
            user_input = f"Think step by step before answering:\n{user_input}"

        # Save user message
        self.history.append({
            "role": "user",
            "content": user_input
        })

        # Generate response
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.history,
            stream=stream
        )

        return response

    # Dummy speech-to-text function
    # (Groq does not support Whisper like OpenAI)
    def speech_to_text(self, audio_path):

        return "Speech-to-text is disabled while using Groq API."

    # Dummy text-to-speech function
    # (Groq does not support OpenAI TTS)
    def text_to_speech(self, text, output_path):

        pass