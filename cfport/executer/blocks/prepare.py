import re
import shutil
import subprocess

from typing import List
from typing import Optional
from pathlib import Path
from cftool.console import ask
from cftool.console import log
from cftool.console import rule

from .download import DownloadBlock
from ..schema import IExecuteBlock
from ...config import IConfig
from ...toolkit import download
from ...toolkit import Platform


@IExecuteBlock.register("prepare")
class PrepareBlock(IExecuteBlock):
    def build(self, config: IConfig) -> None:
        workspace = Path(config.workspace)
        while True:
            if not workspace.is_dir():
                break
            if config.allow_existing:
                log(
                    f"'{workspace}' already exists and `allow_existing` is set to "
                    "`True`, so we will use the existing workspace"
                )
                break
            overwrite = ask(
                f"'{workspace}' already exists, do you want to remove it?",
                choices=["y", "n"],
                default="y",
            )
            if not overwrite:
                workspace = Path(ask("please input a new workspace"))
            else:
                log(f"removing '{workspace}'")
                shutil.rmtree(workspace)
                break
        workspace.mkdir(parents=True, exist_ok=config.allow_existing)


@IExecuteBlock.register("prepare_python")
class PreparePythonBlock(IExecuteBlock):
    root: Path
    executable: Path

    @property
    def download_block(self) -> Optional[DownloadBlock]:
        return self.try_get_previous(DownloadBlock)

    @property
    def pip_cmd(self) -> List[str]:
        return [str(self.executable), "-m", "pip"]

    def build(self, config: IConfig) -> None:
        platform = config.platform
        workspace = Path(config.workspace)
        # windows preparation
        if platform == Platform.WINDOWS:
            download_block = self.download_block
            if download_block is None:
                return
            py_embeddable = download_block.downloaded.get("python_embeddables")
            if py_embeddable is None:
                return
            if len(py_embeddable) != 1:
                raise RuntimeError(
                    "expected download 1 and only 1 python embeddable, "
                    f"but got {len(py_embeddable)}"
                )
            self.root = list(py_embeddable.values())[0]
            self.executable = self.root / "python"
            rule("Preparing Python Embeddable for Windows")
            # modify `_pth` file
            for path in self.root.iterdir():
                if path.suffix != "._pth":
                    continue
                with path.open("r") as f:
                    lines = f.readlines()
                if not lines[-1].startswith("#"):
                    log("Python Embeddable is already prepared")
                    break
                lines.insert(2, ".\Scripts\n")
                lines.insert(3, ".\Lib\site-packages\n")
                lines[-1] = lines[-1][1:]  # remove comment of 'import site'
                with path.open("w") as f:
                    f.writelines(lines)
                break
        # linux / macos preparation
        else:
            rule(f"Creating Python venv for {platform}")
            self.root = workspace / "python_venv"
            self.executable = self.root / "bin" / "python3"
            if self.executable.is_file():
                log("Python venv is already created")
            else:
                subprocess.run(
                    ["python3", "-m", "venv", "--copies", str(self.root.absolute())],
                    check=True,
                )
            bin_dir = self.root / "bin"
            # modify activation scripts
            log("Modifying activation scripts")
            for path in bin_dir.iterdir():
                if path.name.startswith("activate"):
                    with path.open("r") as f:
                        content = f.read()
                    # replace VIRTUAL_ENV with dynamic path
                    content = re.sub(
                        r"VIRTUAL_ENV=[\"\'].*?[\"\']",
                        "VIRTUAL_ENV=$(cd $(dirname $(dirname ${BASH_SOURCE[0]})) && pwd)",
                        content,
                    )
                    with path.open("w") as f:
                        f.write(content)
        # install `pip`
        if subprocess.call(self.pip_cmd, stdout=subprocess.DEVNULL) == 0:
            log("`pip` is already installed")
            return
        log("Installing `pip`")
        temp_dir = workspace / "temp"
        temp_dir.mkdir()
        try:
            get_pip_path = download("https://bootstrap.pypa.io/get-pip.py", temp_dir)
            subprocess.run([self.executable, get_pip_path])
        finally:
            ## remove temp dir
            shutil.rmtree(temp_dir)

    def cleanup(self, config: IConfig) -> None:
        platform = config.platform
        # modify shebangs in scripts
        if platform != Platform.WINDOWS:
            bin_dir = self.root / "bin"
            log("Modifying shebangs in scripts")
            for path in bin_dir.iterdir():
                if not path.is_file() or path.name.startswith("python"):
                    continue
                with path.open("r") as file:
                    lines = file.readlines()
                if lines and lines[0].startswith("#!"):
                    lines[0] = "#!/usr/bin/env python\n"
                    with path.open("w") as file:
                        file.writelines(lines)


class IWithPreparePythonBlock(IExecuteBlock):
    @property
    def prepare_python(self) -> PreparePythonBlock:
        b = self.try_get_previous(PreparePythonBlock)
        if b is None:
            msg = f"`PreparePythonBlock` is required for `{self.__class__.__name__}`"
            raise ValueError(msg)
        return b


__all__ = [
    "PrepareBlock",
    "PreparePythonBlock",
    "IWithPreparePythonBlock",
]
