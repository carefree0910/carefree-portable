from typing import List
from typing import Type
from cftool.pipeline import IPipeline

from .schema import *
from .blocks import *
from ..config import IConfig


def get_default_blocks() -> List[IExecuteBlock]:
    return [
        PrepareBlock(),
        FetchAssetsBlock(),
        DownloadBlock(),
        PreparePythonBlock(),
        InstallPythonRequirementsBlock(),
        HijackHFSpaceAppBlock(),
        SetPythonLaunchScriptBlock(),
    ]


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
        blocks = get_default_blocks()
        if self.config.external_blocks is not None:
            blocks.extend(
                [
                    IExecuteBlock.make(external_block, {})
                    for external_block in self.config.external_blocks
                ]
            )
        return self.build(*blocks)
