import subprocess

from cfport import *
from pathlib import Path
from cfport.toolkit import hijack_file


workspace = "sd_webui_cfport"
webui_block_name = "webui"


@IExecuteBlock.register(webui_block_name)
class WebUIBlock(IExecuteBlock):
    def build(self, config: IConfig) -> None:
        def hijack_python_executable(line: str) -> str:
            if line.startswith("set PYTHON="):
                return f'set PYTHON="{executable}"\n'
            return line

        def hijack_venv_command(line: str) -> str:
            if line.startswith("%PYTHON_FULLNAME% -m venv"):
                return line.replace("venv", "virtualenv")
            return line

        prepare_python = self.try_get_previous(PreparePythonBlock)
        if prepare_python is None:
            raise ValueError("`PreparePythonBlock` is required for `WebUIBlock`")
        workspace = Path(config.workspace)
        # clone repo
        repo_url = "https://github.com/AUTOMATIC1111/stable-diffusion-webui"
        repo_dir = workspace / repo_url.split("/")[-1]
        if not repo_dir.is_dir():
            subprocess.run(["git", "clone", repo_url, str(repo_dir)])
        # hijack python executable
        executable = str(prepare_python.executable)
        executable = executable.replace(config.workspace, "..")
        webui_user_bat = "webui-user.bat"
        hijack_file(repo_dir / webui_user_bat, hijack_python_executable)
        # hijack venv command
        hijack_file(repo_dir / "webui.bat", hijack_venv_command)
        # remove config file
        Path(DEFAULT_CONFIG_FILE).unlink()
        # run installation / launch bat
        subprocess.call([webui_user_bat], cwd=repo_dir, shell=True)


if __name__ == "__main__":
    run_config()
    config = load_config(DEFAULT_CONFIG_FILE)
    config.workspace = workspace
    config.external_blocks = [webui_block_name]
    config.python_requirements = ["virtualenv"]
    config.dump(DEFAULT_CONFIG_FILE)
    run_package(file=DEFAULT_CONFIG_FILE)
