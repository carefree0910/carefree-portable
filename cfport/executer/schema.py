from cftool.pipeline import IBlock

from ..config import IConfig


class IExecuteBlock(IBlock):
    def cleanup(self, config: IConfig) -> None:
        pass


__all__ = [
    "IExecuteBlock",
]
