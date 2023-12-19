from pathlib import Path

from ..schema import IExecuteBlock
from ...config import get_asset
from ...config import IConfig
from ...console import log
from ...console import rule


@IExecuteBlock.register("fetch_assets")
class FetchAssetsBlock(IExecuteBlock):
    def build(self, config: IConfig) -> None:
        assets = config.assets
        if assets is None:
            return
        workspace = Path(config.workspace)
        rule("Fetch Assets")
        for asset in assets:
            asset = get_asset(asset)
            log(f"fetching {asset}")
            asset.fetch(workspace)


__all__ = [
    "FetchAssetsBlock",
]
