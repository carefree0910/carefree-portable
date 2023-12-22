# Stable Diffusion Web UI

This is an example of using `carefree-portable` 📦️ to package the famous [Stable Diffusion Web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) project.

> Currently this example only works on Windows / Linux.


## Target

Run the SD webui locally with one click, without any extra requirements!


## Requirements

- Install [git](https://git-scm.com/download/win).


## Run

```bash
python run.py
```

> - Feel free to run this command multiple times if it crashes in the middle.
> - By the end of the long execution, the Web UI will actually be launched automatically.

This will create an `sd_webui_cfport` directory in the current directory, which is 'out-of-the-box' - simply double click the `webui-user.bat` under the `sd_webui_cfport/stable-diffusion-webui` directory and the Web UI will be started.
