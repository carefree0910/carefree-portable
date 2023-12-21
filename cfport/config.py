import json
import tempfile
import subprocess

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

from .console import log
from .console import rule
from .toolkit import cp
from .toolkit import download
from .toolkit import git_clone
from .toolkit import hijack_cmds
from .toolkit import get_platform
from .toolkit import Platform
from .constants import DEFAULT_WORKSPACE
from .constants import PRESETS_SETTINGS_DIR
from .constants import DEFAULT_SETTINGS_PATH


configs: Dict[str, Type["IConfig"]] = {}


@dataclass
class PyRequirement:
    """
    Represents a Python requirement for a package or module.

    Attributes
    ----------
    git_url : str, optional
        The URL of the Git repository for the requirement.
    package_name : str, optional
        The name of the package for the requirement.
    install_command : str, optional
        The custom installation command for the requirement.
    requirement_file : str, optional
        The path to the requirement file.

    Methods
    -------
    __str__()
        Returns a string representation of the requirement.
    install_with(pip_cmd: List[str], executable: str)
        Installs the requirement using the specified pip command and executable.

    Examples
    --------
    >>> req = PyRequirement(git_url="https://github.com/user/repo.git")
    >>> print(req)
    'https://github.com/user/repo.git'

    >>> req = PyRequirement(package_name="numpy")
    >>> print(req)
    'numpy'

    >>> req = PyRequirement(install_command="pip install mypackage")
    >>> print(req)
    'with install command: pip install mypackage'

    >>> req = PyRequirement(requirement_file="requirements.txt")
    >>> print(req)
    'from requirement file: requirements.txt'

    >>> req.install_with(pip_cmd=["pip"], executable="python")

    """

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

    def install_with(
        self,
        *,
        pip_cmd: List[str],
        executable: str,
    ) -> None:
        rule(f"Installing {self}")
        if self.install_command is not None:
            cmds = self.install_command.split()
            cmds = hijack_cmds(cmds, pip_cmd, executable)
            result = subprocess.run(cmds)
        elif self.git_url is not None:
            result = subprocess.run(pip_cmd + ["install", self.git_url])
        elif self.package_name is not None:
            result = subprocess.run(pip_cmd + ["install", self.package_name])
        elif self.requirement_file is not None:
            result = subprocess.run(pip_cmd + ["install", "-r", self.requirement_file])
        else:
            raise ValueError(f"invalid requirement occurred: {self}")
        if result.returncode != 0:
            raise RuntimeError(f"failed to install requirements: {self}")


def get_py_requirement(req: Union[str, Dict[str, Any], PyRequirement]) -> PyRequirement:
    if isinstance(req, str):
        return PyRequirement(package_name=req)
    if isinstance(req, dict):
        return PyRequirement(**req)
    return req


@dataclass
class Asset:
    """
    Represents an asset with optional attributes such as name, URL, path, Git URL, ignores, flatten, and destination.

    Attributes
    ----------
    name : Optional[str], default=None
        The name of the asset.
    url : Optional[str], default=None
        The URL of the asset.
    path : Optional[str], default=None
        The local path of the asset.
    git_url : Optional[str], default=None
        The Git URL of the asset.
    ignores : Optional[List[str]], default=None
        The list of files or directories to ignore during asset fetching.
    flatten : bool, default=False
        Indicates whether to flatten the asset directory structure during copying.
    dst : Optional[str], default=None
        The destination path of the asset.

    Methods
    -------
    fetch(workspace: Path) -> None
        Fetches the asset and copies it to the specified workspace.

    Examples
    --------
    >>> asset = Asset(url="https://example.com/data.zip")
    >>> asset.fetch(Path("workspace"))
    # No response expected

    >>> asset = Asset(path="local/file.txt")
    >>> asset.fetch(Path("workspace"))
    # No response expected

    >>> asset = Asset(git_url="https://github.com/user/repo.git")
    >>> asset.fetch(Path("workspace"))
    # No response expected

    >>> asset = Asset()
    >>> asset.fetch(Path("workspace"))
    # Raises ValueError: invalid asset occurred: Asset(...)

    """

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
    """
    Represents a configuration for the application.

    This class is not intended to be instantiated directly, it should be generated by the `load_config` function.
    The semantics of the class are documented here for reference, so you can modify the configuration
    JSON files (e.g., `cfport.json`) accordingly.

    Attributes
    ----------
    workspace : str, default=DEFAULT_WORKSPACE
        The workspace path.
    allow_existing : bool, default=True
        Indicates whether to allow existing workspace.
    assets : Optional[List[TAsset]], default=None
        The list of assets to fetch.
    downloads : Dict[str, Union[str, List[str]]], default={}
        The dictionary of download configurations.
    python_requirements : List[Union[str, PyRequirement]], default=[]
        The list of Python requirements.
    huggingface_space_app_file : Optional[str], default=None
        The Hugging Face space app file, if any.
    python_launch_cli : Optional[str], default=None
        The Python launch CLI. It should relative to the `site-packages` directory.
    python_launch_entry : Optional[str], default=None
        The Python launch entry. It should relative to the `workspace`.
    external_blocks : Optional[List[str]], default=None
        The list of external blocks.

    Methods
    -------
    @property
    platform() -> Platform
        Returns the platform of the configuration.

    """

    workspace: str = DEFAULT_WORKSPACE
    allow_existing: bool = True
    assets: Optional[List[TAsset]] = None
    downloads: Dict[str, Union[str, List[str]]] = field(default_factory=dict)
    python_requirements: List[Union[str, PyRequirement]] = field(default_factory=list)
    huggingface_space_app_file: Optional[str] = None
    python_launch_cli: Optional[str] = None
    python_launch_entry: Optional[str] = None
    external_blocks: Optional[List[str]] = None
    version: Optional[str] = None

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
        self._handle_version()

    def dump(self, path: str) -> None:
        with open(path, "w") as f:
            json.dump(self.to_pack().asdict(), f, indent=2)

    def load(self, preset: str) -> None:
        with DEFAULT_SETTINGS_PATH.open("r") as f:
            settings = json.load(f)
        if preset != "none":
            preset_path = PRESETS_SETTINGS_DIR / f"{preset}.json"
            with preset_path.open("r") as f:
                update_dict(json.load(f), settings)
        for k, v in settings.items():
            setattr(self, k, v)
        self._handle_version()

    def _handle_version(self) -> None:
        import cfport

        if self.version is None:
            self.version = cfport.__version__
        elif self.version != cfport.__version__:
            log(
                f"version mismatch: config version is {self.version}, "
                f"but `carefree-portable` 📦️ version is {cfport.__version__}"
            )


@IConfig.register(Platform.LINUX.value)
class LinuxConfig(IConfig):
    pass


@IConfig.register(Platform.WINDOWS.value)
class WindowsConfig(IConfig):
    pass


@IConfig.register(Platform.MACOS.value)
class MacOSConfig(IConfig):
    pass


@IConfig.register("auto")
class AutoConfig(IConfig):
    @property
    def platform(self) -> Platform:
        return get_platform()


def load_config(path: str) -> IConfig:
    with open(path, "r") as f:
        config = json.load(f)
    return IConfig.from_pack(config)


__all__ = [
    "IConfig",
    "LinuxConfig",
    "WindowsConfig",
    "MacOSConfig",
    "AutoConfig",
    "load_config",
]
