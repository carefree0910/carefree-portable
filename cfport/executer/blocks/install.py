from .prepare import IWithPreparePythonBlock
from ..schema import IExecuteBlock
from ...config import IConfig
from ...config import PyRequirement


@IExecuteBlock.register("install_python_requirements")
class InstallPythonRequirementsBlock(IWithPreparePythonBlock):
    def build(self, config: IConfig) -> None:
        pip_cmd = self.prepare_python.pip_cmd
        executable = str(self.prepare_python.executable)
        requirements = config.python_requirements
        for r in requirements:
            if isinstance(r, str):
                r = PyRequirement(package_name=r)
            r.install_with(pip_cmd=pip_cmd, executable=executable)


__all__ = [
    "InstallPythonRequirementsBlock",
]
