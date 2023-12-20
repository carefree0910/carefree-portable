import json
import shutil
import tempfile

from typing import Any
from typing import Dict
from typing import List
from typing import Type
from typing import Union
from typing import Optional
from pathlib import Path
from dataclasses import field
from dataclasses import dataclass
from cftool.misc import update_dict
from cftool.misc import ISerializableDataClass

from .toolkit import cp
from .toolkit import download
from .toolkit import git_clone
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


def get_py_requirement(req: Union[str, Dict[str, Any], PyRequirement]) -> PyRequirement:
    if isinstance(req, str):
        return PyRequirement(package_name=req)
    if isinstance(req, dict):
        return PyRequirement(**req)
    return req


@dataclass
class Asset:
    name: Optional[str] = None
    url: Optional[str] = None
    path: Optional[str] = None
    git_url: Optional[str] = None
    ignores: Optional[List[str]] = None
    flatten: bool = False
    dst: Optional[str] = None

    def fetch(self, workspace: Path) -> None:
        ignores = self.ignores
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_root = Path(tmp_dir)
            if self.path is not None:
                src = Path(self.path)
            elif self.url is not None:
                src = download(self.url, root=tmp_root, name=self.name)
            elif self.git_url is not None:
                git_name = self.name or self.git_url.split("/")[-1]
                src = git_clone(self.git_url, tmp_root / git_name)
                if ignores is None:
                    ignores = [".git"]
            else:
                raise ValueError(f"invalid asset occurred: {self}")
            dst = workspace / Path(self.dst or src.name)
            self.dst = str(dst.relative_to(workspace))
            if src.is_file():
                cp(src, dst)
            else:
                if not self.flatten:
                    cp(src, dst)
                else:
                    if ignores is None:
                        ignores = []
                    for p in src.iterdir():
                        if p.name in ignores:
                            continue
                        cp(p, dst / p.name)


TAsset = Union[str, Dict[str, Any], Asset]


def get_asset(asset: TAsset) -> Asset:
    if isinstance(asset, str):
        return Asset(path=asset)
    if isinstance(asset, dict):
        return Asset(**asset)
    return asset


@dataclass
class IConfig(ISerializableDataClass):
    workspace: str = DEFAULT_WORKSPACE
    allow_existing: bool = True
    assets: Optional[List[TAsset]] = None
    downloads: Dict[str, Union[str, List[str]]] = field(default_factory=dict)
    python_requirements: List[Union[str, PyRequirement]] = field(default_factory=list)
    huggingface_space_app_file: Optional[str] = None
    python_launch_cli: Optional[str] = None
    python_launch_entry: Optional[str] = None
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
        if self.assets is not None:
            self.assets = list(map(get_asset, self.assets))
        self.python_requirements = list(
            map(get_py_requirement, self.python_requirements)
        )

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
