import json

from typing import Dict
from pathlib import Path

from ..schema import IExecuteBlock
from ...config import IConfig
from ...toolkit import download
from ...constants import SETTINGS_DIR


@IExecuteBlock.register("download")
class DownloadBlock(IExecuteBlock):
    downloaded: Dict[str, Dict[str, Path]]

    def build(self, config: IConfig) -> None:
        platform = config.platform
        workspace = Path(config.workspace)
        self.downloaded = {}
        for k, vs in config.downloads.items():
            if isinstance(vs, str):
                vs = [vs]
            k_urls_root = SETTINGS_DIR / "downloads"
            k_urls_path = k_urls_root / f"{k}.json"
            with k_urls_path.open("r") as f:
                k_urls = json.load(f)
            k_workspace = workspace / k
            k_workspace.mkdir(exist_ok=True)
            k_downloaded = self.downloaded.setdefault(k, {})
            for v in vs:
                v_url = k_urls.get(v)
                if isinstance(v_url, dict):
                    v_url = v_url.get(platform.value)
                if v_url is None:
                    raise ValueError(f"[{platform}] cannot find url for '{v}' in '{k}'")
                kv_downloaded = download(v_url, k_workspace)
                k_downloaded[v] = kv_downloaded


__all__ = [
    "DownloadBlock",
]
