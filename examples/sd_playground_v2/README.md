# Playground v2

This is an example of using `carefree-portable` 📦️ to package the brilliant [Playground v2 HuggingFace Space](https://huggingface.co/spaces/playgroundai/playground-v2).


## Target

Start a local gradio app of the [Playground v2 HuggingFace Space](https://huggingface.co/spaces/playgroundai/playground-v2) with one click, without any extra requirements!


## Run

```bash
cfport package -f playground_v2.json
```

> - Feel free to run this command multiple times if it crashes in the middle.
> - If you failed to clone the repo due to network issues, you can try changing the value of `git_url` at L8 of `playground_v2.json` from `https://huggingface.co/spaces/playgroundai/playground-v2` to `git@hf.co:spaces/playgroundai/playground-v2`, and then run the command again.

This will create a `playground_v2_cfport` directory in the current directory, which is 'out-of-the-box' - simply double click the `run.bat` under the `playground_v2_cfport` directory and the target gradio app will be started.

> It may take quite a while to start the app for the first time because many models need to be downloaded and some examples need to be cached first. After that, the app will start in seconds.
