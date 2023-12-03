import gradio as gr

def parse_fn(query):
    return query.upper()


with gr.Blocks() as demo:
    query = gr.Code(label="SQL Query", language=None, interactive=True)
    output = gr.Textbox(label="Parse Result")
    parse_btn = gr.Button("Greet")
    parse_btn.click(fn=parse_fn, inputs=query, outputs=output, api_name="parser")

if __name__ == "__main__":
    demo.launch()
