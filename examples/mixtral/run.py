import gradio as gr

from transformers import AutoTokenizer
from transformers import AutoModelForCausalLM


tag = "mistralai/Mixtral-8x7B"
version = "v0.1"
device = "cuda"

model = AutoModelForCausalLM.from_pretrained(f"{tag}-{version}")
tokenizer = AutoTokenizer.from_pretrained(tag)
model.to(device)


def inference(prompt: str) -> str:
    inputs = tokenizer([prompt], return_tensors="pt").to(device)
    ids = model.generate(**inputs, max_new_tokens=100, do_sample=True)
    return tokenizer.batch_decode(ids)[0]


interface = gr.Interface(
    fn=inference,
    inputs=gr.inputs.Textbox(lines=5, placeholder="Prompt"),
    outputs=gr.outputs.Textbox(),
    title="LLM demo based on Mixtral-8x7B",
)

# Launch the interface
interface.launch()
