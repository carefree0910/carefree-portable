# Contributing

Contributions are truly welcomed! Here are some good (common) ways to get started:

* **GitHub Discussions**: Currently the best way to chat around.
* **GitHub Issues**: Bugs! Fixes! PRs!.

Apart from these, if you want to dive deeper into this project, you can also check out the following sections.

## Installation

It might be necessary to install `carefree-portable` 📦️ from source for development purposes. You can do this by cloning the repository and running `pip install -e .` in the root directory of the repository:

```bash
git clone https://github.com/carefree0910/carefree-portable.git
cd carefree-portable
pip install -e .
```

## Prerequisites

Well, in fact the followings are not actually 'prerequisites', but knowing them will help you understand the system better and improve your contribution experience:

1. [Terminology](https://carefree0910.me/carefree-portable-doc/docs/reference/terminology).
2. The overall [Design Philosophy](https://carefree0910.me/carefree-portable-doc/docs/reference/design-philosophy).

## `JSON` Developers

It might sound weird - but `carefree-portable` 📦️ will hold more `JSON` files than code files by design, since packaging is more of an asset-heavy task, instead of a logic-heavy task.

Please refer to the [JSONs](https://carefree0910.me/carefree-portable-doc/docs/reference/jsons) documentation to see how to add / edit these `JSON` files to suit your needs.

## `Python` Developers

If you find some general packaging logics that cannot be achieved by the existing features, you can create new [`Block`](https://carefree0910.me/carefree-portable-doc/docs/reference/design-philosophy#block)s to extend the system.

As said in the [`Block`](https://carefree0910.me/carefree-portable-doc/docs/reference/design-philosophy#block) documentation, there are two kinds of `Block`s to be created, and their contributing guides will be discussed in the following sections.

### Contribute Default `Block`

There are three steps to contribute your own Default [`Block`](https://carefree0910.me/carefree-portable-doc/docs/reference/design-philosophy#block):

1. Create a file in the `cfport/executer/blocks/third_party` directory, let's say `my_fancy_block.py`.
2. Implement your `Block` (let's say, `MyFancyBlock`), don't forget to register it with `@IExecuteBlock.register("...")` and with a unique name.
3. Expose your `Block` in the `cfport/executer/blocks/third_party/__init__.py` file with `from .my_fancy_block import MyFancyBlock`.
4. Add an instance of your `Block` to the suitable position of the `get_default_blocks` function in the `cfport\executer\__init__.py` file.

### Contribute Specific `Block`

This is simple - just create a folder of the usage of your [`Block`](https://carefree0910.me/carefree-portable-doc/docs/reference/design-philosophy#block) in the `examples` directory, and add a `README.md` file to explain what's going on.

:::note
Check out the [Stable Diffusion Web UI](https://github.com/carefree0910/carefree-portable/blob/main/examples/sd_webui) example for a reference!
:::

### Style Guide

If you are still interested: `carefree-portable` 📦️ adopted [`black`](https://github.com/psf/black) and [`mypy`](https://github.com/python/mypy) to stylize its codes, so you may need to check the format, coding style and type hint with them before your codes could actually be merged.

## Enthusiasts

Although currently `carefree-portable` 📦️ only supports packaging python projects, it is designed to be language-agnostic - it has the full potential to support other languages. By utilizing the existing toolchain, one should be able to easily create a new [`Block`](https://carefree0910.me/carefree-portable-doc/docs/reference/design-philosophy#block) for other languages!
