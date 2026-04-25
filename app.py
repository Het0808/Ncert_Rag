import gradio as gr
from brain import StudyAssistant

# Initialize the assistant
assistant = StudyAssistant()

def predict(message, history):
    # history is a list of [user_message, assistant_message]
    response = ""
    for chunk in assistant.answer(message):
        response += chunk
        yield response

# Define the Gramio Interface
demo = gr.ChatInterface(
    fn=predict, 
    title="PariShiksha: NCERT Study Assistant",
    description="Ask anything about the Class 9 Science 'Motion' chapter. I provide cited answers directly from your textbook.",
    examples=["What is the SI unit of velocity?", "Explain uniform circular motion.", "What does an odometer measure?"],
)

if __name__ == "__main__":
    demo.launch(share=True) # share=True gives a public link too!
