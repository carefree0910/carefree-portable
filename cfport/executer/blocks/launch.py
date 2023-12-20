from pathlib import Path

from .prepare import IWithPreparePythonBlock
from ..schema import IExecuteBlock
from ...config import get_asset
from ...config import IConfig
from ...console import rule
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
            if launch_cli is not None:
                rule(f"Generating '{bat_file}' to run '{launch_cli}' in site-packages")
                cli = self.prepare_python.root / "Lib" / "site-packages" / launch_cli
                cli = str(cli.relative_to(workspace))  # type: ignore
                with bat_path.open("w") as f:
                    f.write(
                        f"""
@echo off
title Run
{executable} {cli} %*
"""
                    )
            elif launch_entry is not None:
                rule(f"Generating '{bat_file}' to run '{launch_entry}'")
                with bat_path.open("w") as f:
                    f.write(
                        f"""
@echo off
title Run
{executable} {launch_entry} %*
"""
                    )


__all__ = [
    "SetPythonLaunchScriptBlock",
]
