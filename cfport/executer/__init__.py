from typing import Type
from cftool.pipeline import IPipeline

from .schema import *
from .blocks import *
from ..config import IConfig


@IPipeline.register("executer")
class Executer(IPipeline):
    config: IConfig

    @classmethod
    def init(cls: Type["Executer"], config: IConfig) -> "Executer":
        self = cls()
        self.config = config
        return self

    @property
    def config_base(self) -> Type[IConfig]:
        return IConfig

    @property
    def block_base(self) -> Type[IExecuteBlock]:
        return IExecuteBlock

    def launch(self) -> None:
        default_blocks = [
            PrepareBlock(),
            FetchAssetsBlock(),
            DownloadBlock(),
            PreparePythonBlock(),
            InstallPythonRequirementsBlock(),
            SetPythonLaunchScriptBlock(),
        ]
        if self.config.external_blocks is not None:
            default_blocks.extend(
                [
                    IExecuteBlock.make(external_block, {})
                    for external_block in self.config.external_blocks
                ]
            )
        return self.build(*default_blocks)
