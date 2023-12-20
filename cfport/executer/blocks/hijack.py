from pathlib import Path

from ..schema import IExecuteBlock
from ...config import IConfig
from ...console import log
from ...toolkit import hijack_file


import_spaces = "import spaces"
decorate_spaces = "@spaces"


def hijack_hf_space_app(line: str) -> str:
    if line.startswith(import_spaces):
        return line[len(import_spaces) :]
    if line.startswith(decorate_spaces):
        return f"# {line}"
    return line


@IExecuteBlock.register("hijack_hf_space_app")
class HijackHFSpaceAppBlock(IExecuteBlock):
    def build(self, config: IConfig) -> None:
        hf_space_app = config.huggingface_space_app_file
        if hf_space_app is None:
            return
        workspace = Path(config.workspace)
        log(f"hijacking huggingface space app file '{hf_space_app}'")
        hijack_file(workspace / hf_space_app, hijack_hf_space_app)


__all__ = [
    "HijackHFSpaceAppBlock",
]
