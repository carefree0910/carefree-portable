from pathlib import Path
from cftool.console import rule

from .prepare import IWithPreparePythonBlock
from ..schema import IExecuteBlock
from ...config import IConfig
from ...toolkit import Platform


@IExecuteBlock.register("set_python_launch_script")
class SetPythonLaunchScriptBlock(IWithPreparePythonBlock):
    def build(self, config: IConfig) -> None:
        platform = config.platform
        workspace = Path(config.workspace)
        launch_cli = config.python_launch_cli
        launch_entry = config.python_launch_entry
        if all(launch is None for launch in (launch_cli, launch_entry)):
            return
        # windows launch
        if platform == Platform.WINDOWS:
            bat_file = "run.bat"
            bat_path = workspace / bat_file
            executable = str(self.prepare_python.executable.relative_to(workspace))
            common_header = f"@echo off\ntitle Run\n"
            if launch_cli is not None:
                rule(f"Generating '{bat_file}' to run '{launch_cli}' in site-packages")
                cli = self.prepare_python.root / "Lib" / "site-packages" / launch_cli
                cli = str(cli.relative_to(workspace))  # type: ignore
                with bat_path.open("w") as f:
                    f.write(
                        f"""{common_header}
{executable} {cli} %*
"""
                    )
            elif launch_entry is not None:
                rule(f"Generating '{bat_file}' to run '{launch_entry}'")
                with bat_path.open("w") as f:
                    f.write(
                        f"""{common_header}
{executable} {launch_entry} %*
"""
                    )
        # linux / macos launch
        else:
            sh_file = "run.sh"
            sh_path = workspace / sh_file
            common_header = f"""#!/bin/bash
source {self.prepare_python.root.relative_to(workspace) / "bin" / "activate"}
which python
"""
            if launch_cli is not None:
                rule(f"Generating '{sh_file}' to run '{launch_cli}' in site-packages")
                lib_dir = self.prepare_python.root / "lib"
                py_dir = next(lib_dir.iterdir())
                cli = py_dir / "site-packages" / launch_cli
                cli = str(cli.relative_to(workspace))  # type: ignore
                with sh_path.open("w") as f:
                    f.write(
                        f"""{common_header}
python {cli} "$@"
"""
                    )
            elif launch_entry is not None:
                rule(f"Generating '{sh_file}' to run '{launch_entry}'")
                with sh_path.open("w") as f:
                    f.write(
                        f"""{common_header}
python {launch_entry} "$@"
"""
                    )


__all__ = [
    "SetPythonLaunchScriptBlock",
]
