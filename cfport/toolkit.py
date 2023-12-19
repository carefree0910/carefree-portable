import sys
import shutil
import subprocess
import urllib.request

from enum import Enum
from typing import Optional
from pathlib import Path
from zipfile import ZipFile
from cftool.misc import DownloadProgressBar

from .console import log


class Platform(str, Enum):
    LINUX = "linux"
    WINDOWS = "windows"
    MACOS = "macos"


def get_platform() -> Platform:
    platform = sys.platform
    if platform.startswith("linux"):
        return Platform.LINUX
    elif platform.startswith("win"):
        return Platform.WINDOWS
    elif platform.startswith("darwin"):
        return Platform.MACOS
    else:
        raise ValueError(f"unknown platform: {platform}")


def download(
    url: str,
    root: Path = Path.cwd(),
    name: Optional[str] = None,
    *,
    remove_zip: bool = True,
) -> Path:
    file = Path(url.split("/")[-1])
    if name is None:
        name = file.stem
    path = root / file
    is_zip = file.suffix == ".zip"
    zip_folder_path = root / name
    if is_zip and zip_folder_path.is_dir():
        log(f"'{zip_folder_path}' already exists, skipping")
        return zip_folder_path
    if not is_zip and path.is_file():
        log(f"'{path}' already exists, skipping")
        return path
    with DownloadProgressBar(unit="B", unit_scale=True, miniters=1, desc=name) as t:
        urllib.request.urlretrieve(
            url,
            filename=path,
            reporthook=t.update_to,
        )
    if not is_zip:
        return path
    with ZipFile(path, "r") as zip_ref:
        zip_ref.extractall(zip_folder_path)
    if remove_zip:
        path.unlink()
    return zip_folder_path


def cp(src: Path, dst: Path) -> None:
    if src.is_file():
        shutil.copyfile(src, dst)
    else:
        shutil.copytree(src, dst)


def git_clone(url: str, dst: Path) -> Path:
    subprocess.run(["git", "lfs", "install"])
    if subprocess.run(["git", "clone", url, str(dst)]).returncode != 0:
        raise RuntimeError(f"failed to clone '{url}'")
    return dst
