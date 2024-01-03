# carefree-portable 📦️

`carefree-portable` 📦️ aims to help you create portable (Python 🐍) projects of your codes / repo!

> 💡We are planning to:
> - ~~use `venv` as a fallback solution for Linux / MacOS.~~ (Done!)
> - support other programming languages in the future, after Python is fully supported.
> 
> See [Roadmap](https://carefree0910.me/carefree-portable-doc/docs/about/roadmap) for more details.


## AI PC

AI PC is a 'new' concept that Intel proposed (see [here](https://www.intel.com/content/www/us/en/products/docs/processors/core-ultra/ai-pc.html)). Since AI PC users often have zero knowledge about programming, it is important to provide them with a portable version of the AI project. This is where `carefree-portable` 📦️ comes in handy!


## Highlights

- **Portable**: The generated portable project can be used directly without any extra requirements.
  - For example, you can run a portable Python project even without Python installed!
- **Extensible**: You can easily extend the functionality of `carefree-portable` 📦️ by editing existing configurations, or adding brand new `block` / `preset` without much effort.
  - See the [Stable Diffusion Web UI](https://github.com/carefree0910/carefree-portable/blob/main/examples/sd_webui) example on how we hijack the famous SD webui repo with a custom `block` and make it portable out-of-the-box.
- **Integrable**: You can integrate `carefree-portable` 📦️ with (GitHub) CI to automatically generate a portable version of your project.
  - Basically, you only need to create a `cfport.json` file in the root directory of your project, and then run `cfport package` in your CI workflow (see [Usages](#usages) for more details).
  - [Here](https://github.com/carefree0910/carefree-portable/blob/main/.github/workflows/package.yml)'s an example of how `carefree-portable` 📦️ packages itself into a portable version in the GitHub CI workflow.


## Installation

`carefree-portable` 📦️ requires Python 3.8 or higher.

```bash
pip install carefree-portable
```

or

```bash
git clone https://github.com/carefree0910/carefree-portable.git
cd carefree-portable
pip install -e .
```


## Usages

> Detailed usages can be found in the [CLI](https://carefree0910.me/carefree-portable-doc/docs/user-guides/cli) & [Configurations](http://localhost:3000/carefree-portable-doc/docs/user-guides/configurations) documentation.

Go to the root directory of your project first:

```bash
cd <path/to/your/project>
```

### Generate Config

To generate a default config, run:

```bash
cfport config
```

This command will genearte a `cfport.json` file in the current directory. To make it work properly, you may need to edit the `python_requirements` field, which is a list of Python packages that your project depends on.

> - Don't forget to add your own project to this field as well!

### Packaging

After generating the config, you can package your project by running:

```bash
cfport package
```

### PyTorch

Since nowadays many fancy projects are built on top of `pytorch`, we provided a preset config for `pytorch` projects, which can be generated by:

```bash
cfport config --preset torch-2.1.0-cu118
# or
cfport config --preset torch-2.1.0-cpu
```

This will generate a `cfport.json` with a pre-defined `requirement` in the `python_requirements` field.

> You may notice that the pre-defined `requirement` starts with `$pip` instead of `pip`. This is important because it can tell `carefree-portable` 📦️ to use the correct `pip` executable when packaging your project.


## Examples

- [mixtral](https://github.com/carefree0910/carefree-portable/blob/main/examples/mixtral), which can generate a portable gradio demo for the famous [`Mixtral-8x7B` LLM](https://huggingface.co/docs/transformers/model_doc/mixtral).
- [Stable Diffusion Web UI](https://github.com/carefree0910/carefree-portable/blob/main/examples/sd_webui), which can generate a portable version of the famous [A1111 webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui).
- [Stable Diffusion - Playground v2](https://github.com/carefree0910/carefree-portable/blob/main/examples/sd_playground_v2), which can generate a portable version of the brilliant [Playground v2 HuggingFace Space](https://huggingface.co/spaces/playgroundai/playground-v2).
  - `Playground v2` itself is a fantastic SD model. It is said that images generated by `Playground v2` are favored **2.5** times more than those produced by SDXL. See their [user study](https://huggingface.co/playgroundai/playground-v2-1024px-aesthetic#user-study) for more details.


## Portable `carefree-portable` 📦️

You may also download the `carefree-portable-*.zip` from the assets of the latest [Releases](https://github.com/carefree0910/carefree-portable/releases). The zip files contain the portable versions of `carefree-portable` 📦️ that can be used directly:
- On Linux / MacOS, you still need to have Python installed (to activate the `venv`), but no extra packages are required.
- On Windows, you can even run it without Python installed!

If you are using this portable version, just make sure to:
- `cd` into the unzipped `carefree-portable-*` folder.
- Replace `cfport` with `.\run.bat` (Windows) / `bash run.sh` (Linux / MacOS) in the following commands.
- Replace `python` with `<path\to\portable\python>` in other python commands. The portable `python` locates at:
  - Windows: `.\carefree-portable-*\python_embeddables\python-3.10.11-embed-amd64\python`.
  - Linux / MacOS: `./carefree-portable-*/python_venv/bin/python3`.

Here's a step by step guide on how to use the portable `carefree-portable` 📦️ to run the [Stable Diffusion Web UI](https://github.com/carefree0910/carefree-portable/blob/main/examples/sd_webui) example:

1. Download the `carefree-portable-*.zip` from the assets of the latest [Releases](https://github.com/carefree0910/carefree-portable/releases).
2. Unzip the `carefree-portable-*.zip` to a folder (let's say, `./carefree-portable-*`), and `cd` into it.
3. Download the `run.py` from [here](https://github.com/carefree0910/carefree-portable/blob/main/examples/sd_webui/run.py), and put it into the unzipped folder (`./carefree-portable-*`).
4. Run the following command, and wait until the webui pops up:

```bash
.\python_embeddables\python-3.10.11-embed-amd64\python run.py
```

5. After these steps, you'll obtain a portable version of the SD webui (locates at `./carefree-portable-*/sd_webui_cfport`), which can be used directly without any extra requirements!


## Contributing

Contributions are truly welcomed!

See [CONTRIBUTING.md](https://github.com/carefree0910/carefree-portable/blob/main/CONTRIBUTING.md) for more details.


## License

`carefree-portable` 📦️ is MIT licensed, as found in the [`LICENSE`](https://github.com/carefree0910/carefree-portable/blob/main/LICENSE) file.

---
