import sys
import shutil
import tarfile
import subprocess
import urllib.request

from enum import Enum
from typing import List
from typing import Callable
from typing import Optional
from pathlib import Path
from zipfile import ZipFile
from cftool.misc import DownloadProgressBar
from cftool.console import log


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
    remove_compressed: bool = True,
) -> Path:
    file = Path(url.split("/")[-1])
    if name is None:
        name = file.stem
    else:
        file = file.with_name(f"{name}{file.suffix}")
    path = root / file
    is_zip = file.suffix == ".zip"
    is_tar = file.suffix in {".tar", ".tar.gz", ".tgz"}
    is_compressed = is_zip or is_tar
    uncompressed_folder_path = root / name
    if is_compressed and uncompressed_folder_path.is_dir():
        log(f"'{uncompressed_folder_path}' already exists, skipping")
        return uncompressed_folder_path
    if not is_compressed and path.is_file():
        log(f"'{path}' already exists, skipping")
        return path
    with DownloadProgressBar(unit="B", unit_scale=True, miniters=1, desc=name) as t:
        urllib.request.urlretrieve(
            url,
            filename=path,
            reporthook=t.update_to,
        )
    if not is_compressed:
        return path
    if is_zip:
        with ZipFile(path, "r") as zip_ref:
            topmost_names = [name for name in zip_ref.namelist() if "/" not in name]
            if topmost_names == [name]:
                dst = root
            else:
                dst = uncompressed_folder_path
            zip_ref.extractall(dst)
    elif is_tar:
        with tarfile.open(path) as tar_ref:
            topmost_names = [name for name in tar_ref.getnames() if "/" not in name]
            if topmost_names == [name]:
                dst = root
            else:
                dst = uncompressed_folder_path
            tar_ref.extractall(dst)
    else:
        raise RuntimeError(f"unknown compressed file type: {file.suffix}")
    if remove_compressed:
        path.unlink()
    return uncompressed_folder_path


def cp(src: Path, dst: Path) -> None:
    if src.is_file():
        shutil.copyfile(src, dst)
    else:
        shutil.copytree(src, dst)


def git_clone(url: str, dst: Path) -> Path:
    if dst.is_dir():
        log(f"'{dst}' already exists, skipping")
        return dst
    subprocess.run(["git", "lfs", "install"])
    if subprocess.run(["git", "clone", url, str(dst)]).returncode != 0:
        raise RuntimeError(f"failed to clone '{url}'")
    return dst


def hijack_file(path: Path, callback: Callable[[str], str]) -> None:
    with path.open("r") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        lines[i] = callback(line)
    with path.open("w") as f:
        f.writelines(lines)


def hijack_cmds(cmds: List[str], pip_cmd: List[str], executable: str) -> List[str]:
    for i, cmd in enumerate(cmds):
        if cmd == "$pip":
            cmds[i] = pip_cmd  # type: ignore
        elif cmd == "$python":
            cmds[i] = executable
    merged = []
    for cmd in cmds:
        if isinstance(cmd, list):
            merged.extend(cmd)
        else:
            merged.append(cmd)
    return merged
