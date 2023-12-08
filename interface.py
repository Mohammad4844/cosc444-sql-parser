from sql_parser_v2 import Parser
import gradio as gr
import re

def parse_fn(query):
    parser = Parser(query)
    parse_output = parser.parse()
    print(parse_output)
    match = re.search(r"Syntax Error at (\d+)", parse_output)
    if match:
        error_token_index = int(match.group(1))
        if error_token_index >= len(parser.input_index_map):
            error_token_index = -1
        start, end = parser.input_index_map[error_token_index]
    
    highlighted_output = []
    for i, q in enumerate(query):
        if match and start <= i <= end - 1:
            highlighted_output.append((q, 'Error'))
        else:
            highlighted_output.append((q, None))
    return parse_output, highlighted_output

with gr.Blocks() as demo:
    query = gr.Code(label="SQL Query", language=None, interactive=True)
    output = gr.Label(label="Parse Result")
    parse_btn = gr.Button("Parse")
    highlighted_output_box = gr.HighlightedText(label="Error", combine_adjacent=True, show_legend=True, color_map={"Error": "red"})
    theme=gr.themes.Base()
    parse_btn.click(fn=parse_fn, inputs=query, outputs=[output, highlighted_output_box], api_name="parser")

if __name__ == "__main__":
    demo.launch()
