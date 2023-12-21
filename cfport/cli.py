import json
import click
import cfport

from cfport import console
from pathlib import Path
from cfport.config import load_config
from cfport.console import log
from cfport.toolkit import get_platform
from cfport.toolkit import Platform
from cfport.constants import PRESETS_SETTINGS_DIR


def run_config(
    *,
    platform: str = "auto",
    preset: str = "none",
    target: str = cfport.DEFAULT_CONFIG_FILE,
) -> None:
    console.rule("Generating Config")
    if platform == "auto":
        platform = get_platform().value
    console.log(f"Target platform: {platform}")
    config: cfport.IConfig = cfport.IConfig.make(platform, {})
    config.load(preset)
    console.log(f"Dumping config to {target}")
    config.dump(target)
    console.log("Done!")


def run_package(*, file: str) -> None:
    console.rule("Packaging Project")
    console.log(f"Loading config from {file}")
    config = load_config(file)
    workspace = config.workspace
    console.log(f"Workspace: {workspace}")
    console.log("Initializing executer")
    executer = cfport.Executer.init(config)
    console.log("Launching executer")
    executer.launch()
    console.log(f"Dumping executer to {workspace}/executer.json")
    with (Path(workspace) / "executer.json").open("w") as f:
        json.dump(executer.to_pack().asdict(), f, indent=2)
    console.rule("Congratulations")
    log("Your portable project is ready!")


def run_execute(*, file: str) -> None:
    console.rule("Packaging Project")
    console.log(f"Launching executer from {file}")
    with open(file, "r") as f:
        cfport.Executer.from_pack(json.load(f))
    console.rule("Congratulations")
    log("Your portable project is ready!")


@click.group()
def main() -> None:
    pass


@main.command()
@click.option(
    "--platform",
    default="auto",
    show_default=True,
    type=click.Choice(["auto"] + [e.value for e in Platform]),
    help="The target platform.",
)
@click.option(
    "--preset",
    default="none",
    show_default=True,
    type=click.Choice(["none"] + [p.stem for p in PRESETS_SETTINGS_DIR.iterdir()]),
    help="The preset config name.",
)
@click.option(
    "-t",
    "--target",
    default=cfport.DEFAULT_CONFIG_FILE,
    show_default=True,
    type=str,
    help="Target output path of the generated config.",
)
def config(
    *,
    platform: str,
    preset: str,
    target: str,
) -> None:
    run_config(platform=platform, preset=preset, target=target)


@main.command()
@click.option(
    "-f",
    "--file",
    default=cfport.DEFAULT_CONFIG_FILE,
    show_default=True,
    type=str,
    help="The config file for packaging.",
)
def package(*, file: str) -> None:
    run_package(file=file)


@main.command()
@click.option(
    "-f",
    "--file",
    type=str,
    help="The executer config file for executing.",
)
def execute(*, file: str) -> None:
    run_execute(file=file)


__all__ = [
    "run_config",
    "run_package",
    "run_execute",
]


if __name__ == "__main__":
    main()
