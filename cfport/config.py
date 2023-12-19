import json

from typing import Any
from typing import Dict
from typing import List
from typing import Type
from typing import Union
from typing import Optional
from dataclasses import field
from dataclasses import dataclass
from cftool.misc import update_dict
from cftool.misc import ISerializableDataClass

from .toolkit import Platform
from .constants import DEFAULT_WORKSPACE
from .constants import PRESETS_SETTINGS_DIR
from .constants import DEFAULT_SETTINGS_PATH


configs: Dict[str, Type["IConfig"]] = {}


@dataclass
class PyRequirement:
    git_url: Optional[str] = None
    package_name: Optional[str] = None
    install_command: Optional[str] = None
    requirement_file: Optional[str] = None

    def __str__(self) -> str:
        if self.install_command is not None:
            return f"with install command: {self.install_command}"
        if self.git_url is not None:
            return self.git_url
        if self.package_name is not None:
            return self.package_name
        if self.requirement_file is not None:
            return f"from requirement file: {self.requirement_file}"
        return super().__str__()

    __repr__ = __str__


@dataclass
class IConfig(ISerializableDataClass):
    workspace: str = DEFAULT_WORKSPACE
    allow_existing: bool = True
    assets: Optional[Dict[str, str]] = None
    downloads: Dict[str, Union[str, Dict[str, str]]] = field(default_factory=dict)
    python_requirements: List[Union[str, PyRequirement]] = field(default_factory=list)
    python_launch_cli: Optional[str] = None
    python_launch_script: Optional[str] = None
    external_blocks: Optional[List[str]] = None

    @classmethod
    def d(cls) -> Dict[str, Type["IConfig"]]:
        return configs

    @property
    def platform(self) -> Platform:
        for p in Platform:
            if p.value == self.__identifier__:
                return p
        raise ValueError(f"unknown config: {self.__identifier__}")

    def from_info(self, info: Dict[str, Any]) -> None:
        super().from_info(info)
        self.python_requirements = [
            requirement
            if isinstance(requirement, str)
            else PyRequirement(**requirement)
            for requirement in self.python_requirements
        ]

    def dump(self, path: str) -> None:
        with open(path, "w") as f:
            json.dump(self.to_pack().asdict(), f, indent=2)

    def load(self, preset: str) -> None:
        with DEFAULT_SETTINGS_PATH.open("r") as f:
            defaults = json.load(f)
        if preset != "none":
            preset_path = PRESETS_SETTINGS_DIR / f"{preset}.json"
            with preset_path.open("r") as f:
                update_dict(json.load(f), defaults)
        for k, v in defaults.items():
            setattr(self, k, v)


@IConfig.register(Platform.LINUX.value)
class LinuxConfig(IConfig):
    pass


@IConfig.register(Platform.WINDOWS.value)
class WindowsConfig(IConfig):
    pass


@IConfig.register(Platform.MACOS.value)
class MacOSConfig(IConfig):
    pass


def load_config(path: str) -> IConfig:
    with open(path, "r") as f:
        config = json.load(f)
    return IConfig.from_pack(config)


__all__ = [
    "IConfig",
    "LinuxConfig",
    "WindowsConfig",
    "MacOSConfig",
    "load_config",
]
