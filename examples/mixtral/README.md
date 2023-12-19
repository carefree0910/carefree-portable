# Mixtral

This is an example of using `carefree-portable` to package the famous [`Mixtral-8x7B` LLM](https://huggingface.co/docs/transformers/model_doc/mixtral).

> Currently this example only works on Windows.


## Target

Start a `Mixtral-8x7B` LLM gradio demo with one click, without any extra requirements!


## Run

```bash
cfport package -f mixtral.json
```

> Feel free to run this command multiple times if it crashes in the middle.

This will create a `mixtral_cfport` directory in the current directory, which is 'out-of-the-box' - simply double click the `run.bat` under the `mixtral_cfport` directory and an LLM gradio demo based on `Mixtral-8x7B` will be started.

> It may take quite a while to start the demo for the first time because many models need to be downloaded first. After that, the demo will start in seconds.
