import subprocess

from cfport import *
from pathlib import Path
from cfport.toolkit import git_clone
from cfport.toolkit import hijack_file
from cfport.toolkit import Platform


workspace = "sd_webui_cfport"
webui_block_name = "webui"


@IExecuteBlock.register(webui_block_name)
class WebUIBlock(IExecuteBlock):
    def build(self, config: IConfig) -> None:
        prepare_python = self.try_get_previous(PreparePythonBlock)
        if prepare_python is None:
            raise RuntimeError("`PreparePythonBlock` is required for `WebUIBlock`")
        platform = config.platform
        workspace = Path(config.workspace)
        # clone repo
        repo_url = "https://github.com/AUTOMATIC1111/stable-diffusion-webui"
        repo_dir = workspace / repo_url.split("/")[-1]
        git_clone(repo_url, repo_dir)
        # hijack python executable
        executable = str(prepare_python.executable)
        executable = executable.replace(config.workspace, "..")
        # windows preparation
        if platform == Platform.WINDOWS:

            def hijack_python_executable(line: str) -> str:
                if line.startswith("set PYTHON="):
                    return f'set PYTHON="{executable}"\n'
                return line

            def hijack_venv_command(line: str) -> str:
                if line.startswith("%PYTHON_FULLNAME% -m venv"):
                    return line.replace("venv", "virtualenv")
                return line

            webui_user_bat = "webui-user.bat"
            hijack_file(repo_dir / webui_user_bat, hijack_python_executable)
            # hijack venv command
            hijack_file(repo_dir / "webui.bat", hijack_venv_command)
            # run installation / launch bat
            subprocess.run([webui_user_bat], cwd=repo_dir, shell=True, check=True)
        # linux / macos preparation
        else:
            command = f"""export python_cmd="{executable}" && bash webui.sh"""
            subprocess.run(command, cwd=repo_dir, shell=True, check=True)


if __name__ == "__main__":
    run_config()
    config = load_config(DEFAULT_CONFIG_FILE)
    config.workspace = workspace
    config.external_blocks = [webui_block_name]
    if config.platform == Platform.WINDOWS:
        config.python_requirements = ["virtualenv"]
    config.dump(DEFAULT_CONFIG_FILE)
    try:
        run_package(file=DEFAULT_CONFIG_FILE)
    finally:
        Path(DEFAULT_CONFIG_FILE).unlink()
