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
        launch_script = config.python_launch_script
        if launch_cli is None and launch_script is None:
            return
        # windows launch
        if platform == Platform.WINDOWS:
            bat_path = workspace / "run.bat"
            executable = str(self.prepare_python.executable.relative_to(workspace))
            if launch_cli is not None:
                rule(f"Generating `.bat` file to run '{launch_cli}'")
                cli = self.prepare_python.root / "Lib" / "site-packages" / launch_cli
                cli = str(cli.relative_to(workspace))
                with bat_path.open("w") as f:
                    f.write(
                        f"""
@echo off
title Run
{executable} {cli} %*
"""
                    )
            elif launch_script is not None:
                launch_script = get_asset(launch_script)
                launch_script.fetch(workspace)
                launch_script_dst = launch_script.dst
                rule(f"Generating `.bat` file to run '{launch_script_dst}'")
                with bat_path.open("w") as f:
                    f.write(
                        f"""
@echo off
title Run
{executable} {launch_script_dst}
"""
                    )


__all__ = [
    "SetPythonLaunchScriptBlock",
]
