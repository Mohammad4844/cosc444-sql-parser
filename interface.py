from sql_parser import Parser
import gradio as gr

def parse_fn(query):
    parser = Parser(query)
    return parser.parse()

with gr.Blocks() as demo:
    query = gr.Code(label="SQL Query", language=None, interactive=True)
    output = gr.Label(label="Parse Result")
    parse_btn = gr.Button("Parse")
    parse_btn.click(fn=parse_fn, inputs=query, outputs=output, api_name="parser")

if __name__ == "__main__":
    demo.launch()
