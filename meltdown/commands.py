from __future__ import annotations

# Standard
import re
from typing import Any
from pathlib import Path
from dataclasses import dataclass

# Modules
from .app import app
from .dialogs import Dialog
from .menus import Menu
from .args import args
from .paths import paths
from .utils import utils
from .files import files


@dataclass
class QueueItem:
    def __init__(self, cmd: str, argument: str) -> None:
        self.cmd = cmd
        self.argument = argument


@dataclass
class Queue:
    def __init__(self, items: list[QueueItem], wait: float = 0.0) -> None:
        self.items = items
        self.wait = wait


class Commands:
    def __init__(self) -> None:
        self.commands: dict[str, dict[str, Any]] = {}
        self.loop_delay = 25
        self.queues: list[Queue] = []
        self.aliases: dict[str, str] = {}

    def setup(self) -> None:
        prefix = utils.escape_regex(args.command_prefix)
        andchar = utils.escape_regex(args.andchar)
        self.cmd_pattern = rf"{andchar}(?= {prefix}\w+)"

        self.make_commands()
        self.make_aliases()
        self.load_file()
        self.start_loop()
        self.get_cmdkeys()

    def get_cmdkeys(self) -> None:
        self.cmdkeys = []

        for key in self.commands:
            self.cmdkeys.append(key)

        for key in self.aliases:
            self.cmdkeys.append(key)

    def start_loop(self) -> None:
        def loop() -> None:
            to_remove = []

            for queue in self.queues:
                if queue.wait:
                    queue.wait -= self.loop_delay

                    if queue.wait <= 0.0:
                        queue.wait = 0.0

                    continue

                if queue.items:
                    item = queue.items.pop(0)

                    if item.cmd == "sleep":
                        if not item.argument:
                            item.argument = "1"

                        if item.argument and queue.items:
                            queue.wait = float(item.argument) * 1000.0
                    elif self.aliases.get(item.cmd):
                        self.exec(self.aliases[item.cmd], queue)
                    elif not self.try_to_run(item.cmd, item.argument):
                        similar = self.get_similar_alias(item.cmd)

                        if similar:
                            self.exec(self.aliases[similar], queue)

                    if not queue.items:
                        to_remove.append(queue)

            for rm_item in to_remove:
                self.queues.remove(rm_item)

            app.root.after(self.loop_delay, lambda: loop())

        loop()

    def make_commands(self) -> None:
        from .command_spec import CommandSpec

        command_spec = CommandSpec()
        self.commands = command_spec.commands

        for key in self.commands:
            self.commands[key]["date"] = 0.0

    def make_aliases(self) -> None:
        for alias in args.aliases:
            key, value = utils.cmd_value(alias)

            if (not key) or (not value):
                continue

            self.aliases[key] = value

    def set_alias(self, cmd: str) -> None:
        from .display import display

        def fmt() -> None:
            display.print("Format: [name] [value]")

        if " " not in cmd:
            fmt()
            return

        name, value = utils.cmd_value(cmd)

        if (not name) or (not value):
            fmt()
            return

        self.aliases[name] = value
        prefix = args.command_prefix
        display.print(f"Set Alias: `{prefix}{name}` is now `{value}`", do_format=True)

    def unset_alias(self, name: str) -> None:
        from .display import display

        if name in self.aliases:
            del self.aliases[name]
            display.print(f"Unset Alias: {name}")
        else:
            display.print(f"Alias not found: {name}")

    def read_alias(self, name: str) -> None:
        from .display import display

        if name in self.aliases:
            display.print(f"Alias: `{name}` is `{self.aliases[name]}`", do_format=True)
        else:
            display.print(f"Alias not found: {name}")

    def is_command(self, text: str) -> bool:
        if len(text) < 2:
            return False

        if "\n" in text:
            return False

        with_prefix = text.startswith(args.command_prefix)
        second_char = text[1:2]
        return with_prefix and second_char.isalpha()

    def exec(self, text: str, queue: Queue | None = None) -> bool:
        text = text.strip()

        if not text:
            return False

        if not self.is_command(text):
            return False

        cmds = re.split(self.cmd_pattern, text)
        items = []

        for item in cmds:
            split = item.strip().split(" ")
            cmd = split[0][1:]
            argument = " ".join(split[1:])
            queue_item = QueueItem(cmd, argument)
            items.append(queue_item)

        if items:
            if queue:
                queue.items = items + queue.items
            else:
                queue = Queue(items)
                self.queues.append(queue)

        return True

    def run(
        self, cmd: str, argument: str | None = None, update_date: bool = False
    ) -> None:
        item = self.commands.get(cmd)

        if not item:
            return

        arg_req = item.get("arg_req")

        if arg_req and (argument in [None, ""]):
            return

        argtype = item.get("type")
        new_argument: Any = None

        if argtype:
            if argtype == "force":
                if argument:
                    new_argument = argument.lower() == "force"
                else:
                    new_argument = False
            elif argument and (argtype is str):
                new_argument = utils.replace_keywords(argument)
            elif argument:
                try:
                    new_argument = argtype(argument)
                except ValueError:
                    return

        item = self.commands[cmd]
        item["action"](new_argument)

        if update_date:
            item["date"] = utils.now()

        self.save_commands()

    def save_commands(self) -> None:
        cmds = {}

        for key in self.commands:
            cmds[key] = {"date": self.commands[key]["date"]}

        files.save(paths.commands, cmds)

    def try_to_run(self, cmd: str, argument: str) -> bool:
        for key in self.commands:
            if cmd == key:
                self.run(key, argument)
                return True

        most_similar = utils.most_similar(cmd, list(self.commands.keys()))

        if most_similar:
            self.run(most_similar, argument)
            return True

        return False

    def get_similar_alias(self, cmd: str) -> str | None:
        return utils.most_similar(cmd, list(self.aliases.keys()))

    def help(self) -> None:
        from .model import model

        text = utils.replace_keywords(args.help_prompt)
        prompt = {"text": text}
        model.stream(prompt)

    def show_help(
        self, tab_id: str | None = None, filter_text: str | None = None
    ) -> None:
        from .display import display

        text = self.get_commandtext(filter_text)
        display.print(text, tab_id=tab_id)
        display.format_text(tab_id=tab_id, mode="all")

    def make_palette(self) -> None:
        self.palette = Menu()

        def add_item(key: str) -> None:
            cmd = self.commands[key]

            if cmd.get("skip_palette"):
                return

            def command() -> None:
                if cmd.get("arg_req"):
                    Dialog.show_input("Argument", lambda a: self.run(key, a))
                else:
                    self.run(key, update_date=True)

            if args.alt_palette:
                text = key
                tooltip = cmd["info"]
            else:
                text = cmd["info"]
                tooltip = key

            self.palette.add(text=text, command=lambda e: command(), tooltip=tooltip)

        keys = sorted(
            self.commands, key=lambda x: self.commands[x]["date"], reverse=True
        )

        for key in keys:
            add_item(key)

    def show_palette(self) -> None:
        from .widgets import widgets

        self.make_palette()
        self.palette.show(widget=widgets.main_menu_button)

    def cmd(self, text: str) -> str:
        return args.command_prefix + text

    def load_file(self) -> None:
        if (not paths.commands.exists()) or (not paths.commands.is_file()):
            return

        try:
            cmds = files.load(paths.commands)
        except BaseException as e:
            utils.error(e)
            cmds = {}

        for key in cmds:
            if key in self.commands:
                self.commands[key]["date"] = cmds[key].get("date", 0.0)

    def get_commandtext(self, filter_text: str | None = None) -> str:
        sep = "\n\n---\n\n"
        text = ""

        if not filter_text:
            text += "# Commands\n\n"
            text += "Commands can be chained:\n\n"

            text += "```\n"
            text += "/tab 2 & /sleep 0.5 & /select\n"
            text += "```\n\n"

            text += "This will select tab 2, then wait 500ms, then select all.\n\n"

            text += "Here are all the available commands:"

        for key in self.commands:
            cmd = self.commands[key]
            txt = ""
            txt += sep
            txt += f"### {key}\n\n"
            txt += cmd["info"]
            extra = cmd.get("extra")

            if extra:
                txt += f"\n\n{extra}"

            if filter_text:
                if filter_text.lower() not in txt.lower():
                    continue

            text += txt

        text += "\n"
        return text.lstrip()

    def make_commandoc(self, pathstr: str) -> None:
        from .display import display

        path = Path(pathstr)

        if (not path.parent.exists()) or (not path.parent.is_dir()):
            utils.msg(f"Invalid path: {pathstr}")
            return

        text = self.get_commandtext()
        files.write(path, text)
        msg = f"Saved to {path}"
        display.print(msg)
        utils.msg(msg)

    def after_stream(self) -> None:
        if args.after_stream:
            app.root.after(100, lambda: self.exec(args.after_stream))


commands = Commands()
