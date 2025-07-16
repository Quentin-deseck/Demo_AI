import gradio as gr

def image_classifier(inp):
    return {'cat': 0.3, 'dog': 0.7}

inputs=[gr.image(),'image']

demo = gr.Interface(
    fn=image_classifier, 
    inputs=inputs, 
    outputs="label")
demo.launch()