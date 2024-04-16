# Standard
import json
from typing import Any, Optional, List, Dict

# Modules
from .tooltips import ToolTip
from .commands import commands
from .config import config
from .entrybox import EntryBox
from .app import app
from .args import args
from .paths import paths
from .dialogs import Dialog
from .tips import tips
from .utils import utils
from .files import files
from . import widgetutils


class InputControl:
    def __init__(self) -> None:
        self.history_index = -1
        self.input: EntryBox
        self.autocomplete: List[str] = []

    def fill(self) -> None:
        from .widgets import widgets

        frame_data = widgets.frame_data_input
        self.input_label = widgetutils.make_label(frame_data, "Input")

        self.input = widgetutils.make_entry(frame_data)
        frame_data.expand()
        widgets.input = self.input
        widgets.input_frame = frame_data.frame
        ToolTip(self.input_label, tips["input"])
        ToolTip(self.input, tips["input"])

        prev_button = widgetutils.make_button(
            frame_data, "< Prev", lambda: self.history_up()
        )
        ToolTip(prev_button, tips["prev_button"])

        next_button = widgetutils.make_button(
            frame_data, "Next >", lambda: self.history_down()
        )
        ToolTip(next_button, tips["next_button"])

        if args.write_button:
            write_button = widgetutils.make_button(
                frame_data, "Write", lambda: self.show_textbox()
            )
            ToolTip(write_button, tips["write_button"])

        submit_button = widgetutils.make_button(
            frame_data,
            "Submit",
            lambda: self.submit(scroll=False),
            right_padding=app.theme.right_padding,
        )

        ToolTip(submit_button, tips["submit_button"])

    def wheel_up(self) -> None:
        ToolTip.hide_all()
        self.history_down()

    def wheel_down(self) -> None:
        ToolTip.hide_all()
        self.history_up()

    def bind(self) -> None:
        self.input.bind("<Button-3>", lambda e: self.show_menu(e))
        self.input.bind("<Button-4>", lambda e: self.wheel_up())
        self.input.bind("<Button-5>", lambda e: self.wheel_down())

    def show_menu(self, event: Optional[Any] = None) -> None:
        from .widgets import widgets

        widgets.show_menu_items("input", "inputs", lambda s: self.set(s), event)

    def focus(self) -> None:
        self.input.focus_set()

    def apply_history(self) -> None:
        inputs = files.get_list("inputs")
        text = inputs[self.history_index]
        self.set(text)

    def history_up(self) -> None:
        inputs = files.get_list("inputs")

        if not self.input.get():
            self.reset_history_index()

        if not inputs:
            return

        if self.history_index == -1:
            self.history_index = 0
        else:
            if self.history_index == len(inputs) - 1:
                self.clear()
                return
            else:
                self.history_index = (self.history_index + 1) % len(inputs)

        self.apply_history()

    def history_down(self) -> None:
        inputs = files.get_list("inputs")

        if not inputs:
            return

        if self.history_index == -1:
            self.history_index = len(inputs) - 1
        else:
            if self.history_index == 0:
                self.clear()
                return
            else:
                self.history_index = (self.history_index - 1) % len(inputs)

        self.apply_history()

    def set(self, text: str) -> None:
        self.input.set_text(text)
        self.focus()

    def clear(self) -> None:
        self.input.clear()
        self.reset_history_index()

    def reset_history_index(self) -> None:
        self.history_index = -1

    def insert_name(self, who: str) -> None:
        name = getattr(config, f"name_{who}")
        text = self.input.get()

        if (not text) or text.endswith(" "):
            self.input.insert_text(name)
        else:
            self.input.insert_text(f" {name}")

        self.input.full_focus()

    def submit(self, tab_id: str = "", text: str = "", scroll: bool = True) -> None:
        from .model import model
        from .display import display

        if args.display:
            if not text:
                if scroll:
                    display.toggle_scroll()

                return

        if not text:
            text = self.input.get().strip()

        if not tab_id:
            tab_id = display.current_tab

        tab = display.get_tab(tab_id)

        if not tab:
            return

        if text:
            self.clear()
            files.add_input(text)
            self.add_words(text)

            if args.commands:
                if commands.exec(text):
                    return

            if tab.mode == "ignore":
                return

            display.to_bottom()

            if model.model_loading:
                return

            model.stream(text, tab.tab_id)
        elif scroll:
            display.toggle_scroll()

    def setup(self) -> None:
        path = paths.autocomplete

        if path.exists() and path.is_file():
            with open(path, "r", encoding="utf-8") as file:
                try:
                    self.autocomplete = json.load(file)
                except BaseException as e:
                    utils.error(e)
                    self.autocomplete = []
        else:
            self.autocomplete = []

        self.check()

    def check(self) -> None:
        from .display import display

        text = args.input.strip()

        if not text:
            return

        tab_id = display.current_tab

        if args.clean_slate:
            is_command = commands.is_command(text)

            if not is_command:
                if not display.tab_is_empty(tab_id):
                    tab_id = display.make_tab()

        self.submit(tab_id=tab_id, text=text)

    def add_words(self, text: str) -> None:
        from . import terminal

        if not args.input_memory:
            return

        words = text.split()
        added = False

        for word in words:
            len_words = len(word)

            if len_words < args.input_memory_min:
                continue

            if len_words > config.input_memory_max:
                continue

            if commands.is_command(word):
                continue

            if word not in self.autocomplete:
                self.autocomplete.append(word)
                terminal.add_word(word)
                added = True

        if added:
            files.save(paths.autocomplete, self.autocomplete)

    def show_textbox(self) -> None:
        def action(ans: Dict[str, Any]) -> None:
            self.submit(text=ans["text"], scroll=False)

        text = self.input.get().strip()
        self.clear()
        Dialog.show_textbox("Write an input", lambda a: action(a), value=text)

    def input_command(self, arg: str) -> None:
        if arg:
            self.submit(text=arg)
        else:
            self.show_textbox()

    def paste(self) -> None:
        utils.paste(self.input)


inputcontrol = InputControl()
