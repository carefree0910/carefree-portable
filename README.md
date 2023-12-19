# carefree-portable

`carefree-portable` aims to help you create portable (Python 🐍) projects of your codes / repo!

> Currently we only support packaging Python projects on Windows because Python only provides embeddable Python for Windows officially. But as far as I know there exists some embeddable Python for Linux / MacOS as well, so I'll look into them in the future.

> Maybe other programming languages will also be supported in the future, after Python is fully supported.


## Highlights

- **Portable**: The generated portable project can be used directly without any extra requirements.
  - For example, you can run a portable Python project even without Python installed!
- **Extensible**: You can easily extend the functionality of `carefree-portable` by editing existing configurations, or adding brand new `block` / `preset` without much effort.
  - See the [Stable Diffusion Web UI](https://github.com/carefree0910/carefree-portable/blob/main/examples/sd_webui) example on how we hijack the famous SD webui repo with a custom `block` and make it portable out-of-the-box!
- **Integrable**: You can integrate `carefree-portable` with (GitHub) CI to automatically generate a portable version of your project.
  - Basically, you only need to create a `cfport.json` file in the root directory of your project, and then run `cfport package` in your CI workflow (see [Usages](#usages) for more details).
  - [Here](https://github.com/carefree0910/carefree-portable/blob/main/.github/workflows/package.yml)'s an example of how `carefree-portable` packages itself into a portable version in the GitHub CI workflow!


## Installation

`carefree-portable` requires Python 3.8 or higher.

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

> Detailed usages can be found in the [Wiki](https://github.com/carefree0910/carefree-portable/wiki) page.

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

> - You may notice that the default `install_command` starts with `$pip` instead of `pip`. This is important because it can tell `carefree-portable` to use the correct `pip` executable when packaging your project.
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

> Again, you may notice that the pre-defined `requirement` starts with `$pip` instead of `pip`. This is important because it can tell `carefree-portable` to use the correct `pip` executable when packaging your project.


## Examples

- [mixtral](https://github.com/carefree0910/carefree-portable/blob/main/examples/mixtral), which can generate a portable service for the famous [`Mixtral-8x7B` LLM](https://huggingface.co/docs/transformers/model_doc/mixtral).
- [Stable Diffusion Web UI](https://github.com/carefree0910/carefree-portable/blob/main/examples/sd_webui), which can generate a portable version of the famous [A1111 webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui).


## Portable `carefree-portable`

If you are Windows user, you may also download the `carefree-portable.zip` from the assets of the latest [Releases](https://github.com/carefree0910/carefree-portable/releases). This zip file contains a portable version of `carefree-portable` that can be used directly without any extra requirements - you can even run it without Python installed!

If you are using this portable version, just make sure to:
- `cd` into the unzipped `carefree-portable` folder.
- Replace `cfport` with `.\run.bat` in the following commands.
- Replace `python` with `<path\to\portable\python>` in other python commands.
  - The portable `python` locates at `.\carefree-portable\python_embeddables\python-3.10.11-embed-amd64\python`.

Here's a step by step guide on how to use the portable `carefree-portable` to run the [Stable Diffusion Web UI](https://github.com/carefree0910/carefree-portable/blob/main/examples/sd_webui) example:

1. Download the `carefree-portable.zip` from the assets of the latest [Releases](https://github.com/carefree0910/carefree-portable/releases).
2. Unzip the `carefree-portable.zip` to a folder (let's say, `./carefree-portable`), and `cd` into it.
3. Download the `run.py` from [here](https://github.com/carefree0910/carefree-portable/blob/main/examples/sd_webui/run.py), and put it into the unzipped folder (`./carefree-portable`).
4. Run the following command, and wait until the webui pops up:

```bash
.\python_embeddables\python-3.10.11-embed-amd64\python run.py
```

5. After these steps, you'll obtain a portable version of the SD webui (locates at `./carefree-portable/sd_webui_cfport`), which can be used directly without any extra requirements!


## Contributing

Contributions are truly welcomed!

Since this project is mainly a JSON-based project, so in most cases contributions could be made by simply adding / editing various JSON files. It'll also be great if you can provide some examples for the new features you added.

See [CONTRIBUTING.md](https://github.com/carefree0910/carefree-portable/blob/main/CONTRIBUTING.md) for more details.


## License

`carefree-portable` is MIT licensed, as found in the [`LICENSE`](https://github.com/carefree0910/carefree-portable/blob/main/LICENSE) file.

---
