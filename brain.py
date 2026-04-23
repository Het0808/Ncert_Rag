import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class StudyAssistant:
    def __init__(self, model="llama-3.3-70b-versatile"):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = model

    def ask_with_context(self, question, context):
        """
        Sends a question and context to Groq and streams the response.
        """
        system_prompt = (
            "You are PariShiksha, an expert NCERT Science Assistant. "
            "Use the provided context to answer the user's question accurately. "
            "If the answer is not in the context, say you don't know based on the provided material."
        )
        
        user_content = f"Context: {context}\n\nQuestion: {question}"

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0,
            max_completion_tokens=8192,
            top_p=1,
            stream=True
        )

        for chunk in completion:
            content = chunk.choices[0].delta.content
            if content:
                yield content

if __name__ == "__main__":
    # Test call
    assistant = StudyAssistant()
    print("AI Assistant response: ", end="")
    for text in assistant.ask_with_context("What is motion?", "Motion is the change in position of an object over time."):
        print(text, end="", flush=True)
