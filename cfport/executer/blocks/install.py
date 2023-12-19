import subprocess

from typing import List

from .prepare import PreparePythonBlock
from .prepare import IWithPreparePythonBlock
from ..schema import IExecuteBlock
from ...config import IConfig
from ...config import PyRequirement
from ...console import rule


def hijack_cmds(cmds: List[str], prepare_python: PreparePythonBlock) -> List[str]:
    for i, cmd in enumerate(cmds):
        if cmd == "$pip":
            cmds[i] = prepare_python.pip_cmd
        elif cmd == "$python":
            cmds[i] = str(prepare_python.executable)
    merged = []
    for cmd in cmds:
        if isinstance(cmd, list):
            merged.extend(cmd)
        else:
            merged.append(cmd)
    return merged


@IExecuteBlock.register("install_python_requirements")
class InstallPythonRequirementsBlock(IWithPreparePythonBlock):
    def build(self, config: IConfig) -> None:
        requirements = config.python_requirements
        for r in requirements:
            if isinstance(r, str):
                r = PyRequirement(package_name=r)
            self.handle(r)

    def handle(self, r: PyRequirement) -> None:
        rule(f"Installing {r}")
        pip_cmd = self.prepare_python.pip_cmd
        if r.install_command is not None:
            cmds = r.install_command.split()
            cmds = hijack_cmds(cmds, self.prepare_python)
            result = subprocess.run(cmds)
        elif r.git_url is not None:
            result = subprocess.run(pip_cmd + ["install", r.git_url])
        elif r.package_name is not None:
            result = subprocess.run(pip_cmd + ["install", r.package_name])
        elif r.requirement_file is not None:
            result = subprocess.run(pip_cmd + ["install", "-r", r.requirement_file])
        else:
            raise ValueError(f"invalid requirement occurred: {r}")
        if result.returncode != 0:
            raise RuntimeError(f"failed to install requirements: {r}")


__all__ = [
    "InstallPythonRequirementsBlock",
]
