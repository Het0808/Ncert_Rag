import gradio as gr
from brain import StudyAssistant
import os

assistant = StudyAssistant()

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Reset & Base */
body, .gradio-container {
    font-family: 'Inter', sans-serif !important;
    background-color: #0d0f1a !important;
    color: #e2e8f0 !important;
}

/* Hide Gradio Footer */
footer { display: none !important; }

/* Force Chatbot Text Visibility */
.prose, .prose * {
    color: #e2e8f0 !important;
}

/* Custom Layout Classes */
.ps-shell {
    max-width: 1400px;
    margin: 0 auto;
    border: 1px solid #1e293b;
    border-radius: 12px;
    overflow: hidden;
    background-color: #0d0f1a;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.ps-sidebar {
    background-color: #111827 !important;
    border-right: 1px solid #1e293b !important;
    padding: 20px !important;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.ps-main {
    background-color: #0d0f1a !important;
    display: flex;
    flex-direction: column;
}

.ps-topbar {
    background-color: #111827 !important;
    border-bottom: 1px solid #1e293b !important;
    padding: 16px 24px !important;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* Typography */
.ps-logo-text {
    font-size: 1.5rem;
    font-weight: 700;
    background: linear-gradient(90deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.ps-logo-sub {
    font-size: 0.8rem;
    color: #64748b;
    display: block;
    margin-top: 4px;
}

/* Buttons */
.ps-btn-primary {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #ffffff !important;
    border: none !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
.ps-btn-primary:hover { opacity: 0.9 !important; }

.ps-btn-secondary {
    background-color: #1e293b !important;
    color: #cbd5e1 !important;
    border: 1px solid #334155 !important;
    transition: all 0.2s !important;
}
.ps-btn-secondary:hover { background-color: #334155 !important; color: #f1f5f9 !important; }

.ps-btn-ghost {
    background: transparent !important;
    color: #94a3b8 !important;
    border: 1px solid transparent !important;
    text-align: left !important;
    justify-content: flex-start !important;
}
.ps-btn-ghost:hover { background-color: #1e293b !important; color: #e2e8f0 !important; }

/* Input Area */
.ps-input-area {
    background-color: #111827 !important;
    border-top: 1px solid #1e293b !important;
    padding: 20px 24px !important;
}

.ps-textbox textarea {
    background-color: #1e293b !important;
    color: #e2e8f0 !important;
    border: 1px solid #334155 !important;
}
.ps-textbox textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.2) !important;
}

/* Stats */
.ps-stats {
    display: flex;
    gap: 20px;
    padding: 12px 24px;
    background-color: #0a0c15;
    border-top: 1px solid #1e293b;
    font-size: 0.8rem;
    color: #475569;
}
"""

EXAMPLES = [
    "What is motion? Give the definition.",
    "What is the SI unit of velocity?",
    "Explain distance vs displacement.",
    "What is uniform vs non-uniform motion?",
    "Derive the equations of motion.",
    "What does an odometer measure?",
]

def predict(message, history):
    if not message:
        yield "", history
        return
        
    history = history or []
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": ""})
    
    yield "", history

    response = ""
    for chunk in assistant.answer(message):
        response += chunk
        history[-1]["content"] = response
        yield "", history

def clear_chat():
    return []

with gr.Blocks(css=CSS, theme=gr.themes.Base()) as demo:
    
    with gr.Row(elem_classes="ps-shell"):
        
        # --- SIDEBAR ---
        with gr.Column(scale=0, min_width=280, elem_classes="ps-sidebar"):
            gr.HTML("""
            <div style="margin-bottom: 16px;">
              <span class="ps-logo-text">📚 PariShiksha</span>
              <span class="ps-logo-sub">NCERT Class 9 · Motion Chapter</span>
            </div>
            """)
            
            new_chat_btn = gr.Button("＋ New Chat", elem_classes="ps-btn-primary")
            
            gr.Markdown("### Topics")
            
            topic_btns = [
                gr.Button("🔵 Motion Basics", elem_classes="ps-btn-ghost"),
                gr.Button("🟣 Velocity & Speed", elem_classes="ps-btn-ghost"),
                gr.Button("🟡 Equations of Motion", elem_classes="ps-btn-ghost"),
                gr.Button("🟢 Circular Motion", elem_classes="ps-btn-ghost")
            ]
            
        # --- MAIN PANEL ---
        with gr.Column(scale=1, elem_classes="ps-main"):
            
            # Topbar
            with gr.Row(elem_classes="ps-topbar"):
                gr.HTML("""
                <div style="font-weight: 600; font-size: 1.1rem; display: flex; align-items: center; gap: 8px;">
                  Motion Chapter
                  <span style="font-size: 0.7rem; background: rgba(99,102,241,0.2); padding: 2px 8px; border-radius: 12px; border: 1px solid rgba(99,102,241,0.4); color: #a5b4fc;">NCERT</span>
                </div>
                """)
                with gr.Row():
                    top_new_chat_btn = gr.Button("＋ New Chat", elem_classes="ps-btn-secondary", size="sm")
                    
                    # Copy to clipboard via JS
                    share_js = "(...args) => { navigator.clipboard.writeText(window.location.href); alert('Link copied to clipboard!'); return args; }"
                    share_btn = gr.Button("⬆ Share", elem_classes="ps-btn-secondary", size="sm")
                    share_btn.click(None, None, None, js=share_js)
            
            # Chatbot
            chatbot = gr.Chatbot(
                show_label=False,
                height=500,
                avatar_images=(None, "https://api.dicebear.com/7.x/bottts/svg?seed=PariShiksha&backgroundColor=6366f1"),
                placeholder="Ask PariShiksha! Your questions about the Motion chapter answered with citations."
            )
            
            # Input Area
            with gr.Column(elem_classes="ps-input-area"):
                
                # Examples
                gr.Markdown("**Suggested Questions:**", elem_classes="ps-logo-sub")
                with gr.Row():
                    example_btns = []
                    for ex in EXAMPLES:
                        btn = gr.Button(ex, elem_classes="ps-btn-secondary", size="sm")
                        example_btns.append(btn)
                
                # Textbox and Submit
                with gr.Row():
                    txt = gr.Textbox(
                        show_label=False,
                        placeholder="Ask anything about the Motion chapter...",
                        container=False,
                        scale=8,
                        elem_classes="ps-textbox"
                    )
                    send_btn = gr.Button("Ask ✨", elem_classes="ps-btn-primary", scale=1)
            
            # Footer stats
            gr.HTML("""
            <div class="ps-stats">
              <div>⚡ BM25 Retrieval</div>
              <div>🧠 Llama 3.1 8B</div>
              <div>📄 46 Indexed Chunks</div>
              <div>📑 NCERT Curriculum</div>
            </div>
            """)

    # --- EVENT BINDINGS ---
    
    # Process message from textbox enter key
    txt.submit(predict, [txt, chatbot], [txt, chatbot], queue=True)
    # Process message from submit button
    send_btn.click(predict, [txt, chatbot], [txt, chatbot], queue=True)
    
    # Clear chat functionality
    new_chat_btn.click(clear_chat, None, [chatbot], queue=False)
    top_new_chat_btn.click(clear_chat, None, [chatbot], queue=False)
    
    # Topic buttons populate textbox and submit
    topics = ["What is motion?", "Explain velocity and speed.", "Derive equations of motion.", "What is uniform circular motion?"]
    for btn, topic_text in zip(topic_btns, topics):
        btn.click(lambda text=topic_text: text, None, [txt], queue=False).then(
            predict, [txt, chatbot], [txt, chatbot], queue=True
        )
        
    # Example buttons populate textbox and submit
    for btn, ex_text in zip(example_btns, EXAMPLES):
        btn.click(lambda text=ex_text: text, None, [txt], queue=False).then(
            predict, [txt, chatbot], [txt, chatbot], queue=True
        )

if __name__ == "__main__":
    # Use host=0.0.0.0 to ensure accessibility, share=False since we are running locally
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
