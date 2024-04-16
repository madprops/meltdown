# Standard
import os
import json
from typing import Any
from pathlib import Path

# Modules
from .paths import paths
from .config import config
from .args import args
from .utils import utils


class Files:
    def __init__(self) -> None:
        self.models_list = []
        self.inputs_list = []
        self.systems_list = []
        self.prepends_list = []
        self.appends_list = []

    def save(self, path: Path, dictionary: Any) -> None:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(dictionary, file, indent=4)

    def load(self) -> None:
        if args.config:
            config.load_arg()
        else:
            config.load_file()

        self.load_models_file()
        self.load_inputs_file()
        self.load_systems_file()
        self.load_prepends_file()
        self.load_appends_file()

    def load_models_file(self) -> None:
        from .model import model

        self.load_list_file(paths.models, "models")
        model.check_config()

    def load_inputs_file(self) -> None:
        self.load_list_file(paths.inputs, "inputs")

    def load_systems_file(self) -> None:
        self.load_list_file(paths.systems, "systems")

    def load_prepends_file(self) -> None:
        self.load_list_file(paths.prepends, "prepends")

    def load_appends_file(self) -> None:
        self.load_list_file(paths.appends, "appends")

    def load_list_file(self, path: Path, key: str) -> None:
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)

        with open(path, "r", encoding="utf-8") as file:
            name = f"{key}_list"

            try:
                items = json.load(file)
            except BaseException as e:
                utils.error(e)
                items = []

                if hasattr(self, name):
                    item = getattr(self, name)

                    if item:
                        items.append(item)

            setattr(self, name, items)

    def add_model(self, text: str) -> None:
        self.add_to_list("models", text)

    def add_input(self, text: str) -> None:
        self.add_to_list("inputs", text)

    def add_system(self, text: str) -> None:
        self.add_to_list("systems", text)

    def add_prepends(self, text: str) -> None:
        self.add_to_list("prepends", text)

    def add_appends(self, text: str) -> None:
        self.add_to_list("appends", text)

    def add_to_list(self, key: str, text: str) -> None:
        if not text:
            return

        name = f"{key}_list"
        items = getattr(self, name)
        new_items = [item for item in items if item != text]
        new_items.insert(0, text)
        new_items = new_items[: config.max_file_list]
        setattr(self, name, new_items)
        path = getattr(paths, key)
        self.save(path, new_items)

    def open_log(self, name: str = "") -> None:
        from .app import app

        path = paths.logs
        path.mkdir(parents=True, exist_ok=True)
        os_name = os.name.lower()

        if name:
            path = Path(path, name)

        spath = str(path)

        if os_name == "posix":
            # Linux
            app.run_command(["xdg-open", spath])
        elif os_name == "nt":
            # Windows
            app.run_command(["start", spath])
        elif os_name == "darwin":
            # macOS
            app.run_command(["open", spath])
        else:
            utils.error(f"Unrecognized OS: {os_name}")


files = Files()