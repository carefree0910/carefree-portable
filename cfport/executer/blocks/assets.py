import shutil

from pathlib import Path

from ..schema import IExecuteBlock
from ...config import IConfig
from ...console import log
from ...console import rule


@IExecuteBlock.register("copy_assets")
class CopyAssetsBlock(IExecuteBlock):
    def build(self, config: IConfig) -> None:
        assets = config.assets
        if assets is None:
            return
        workspace = Path(config.workspace)
        rule("Copying Assets")
        for src, dst in assets.items():
            dst_path = workspace / dst
            log(f"copying {src} to {dst_path}")
            shutil.copyfile(src, dst_path)


__all__ = [
    "CopyAssetsBlock",
]
