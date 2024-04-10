# Standard
import json
from typing import Any, Optional, List

# Modules
from .tooltips import ToolTip
from .commands import commands
from .config import config
from .entrybox import EntryBox
from .app import app
from .args import args
from .paths import paths
from .dialogs import Dialog
from . import widgetutils
from . import filemanager


class InputControl:
    def __init__(self) -> None:
        self.history_index = -1
        self.input: EntryBox
        self.autocomplete: List[str] = []

    def fill(self) -> None:
        from .widgets import widgets

        frame_data = widgets.frame_data_input
        self.input_label = widgetutils.make_label(frame_data, "Input")

        if args.textbox_button:
            textbox_button = widgetutils.make_button(frame_data, "#", lambda: self.show_textbox())
            ToolTip(textbox_button, "Show a textbox for longer inputs")

        self.input = widgetutils.make_entry(frame_data)
        frame_data.expand()
        widgets.input = self.input
        widgets.input_frame = frame_data.frame
        tip = "The prompt for the AI." \
            " The prompt is a message that the AI will respond to." \
            " Use the mousewheel to cycle input history"
        ToolTip(self.input_label, tip)
        ToolTip(self.input, tip)

        prev_button = widgetutils.make_button(frame_data, "< Prev", lambda: self.history_up())
        ToolTip(prev_button, "Previous item in the input history")

        next_button = widgetutils.make_button(frame_data, "Next >", lambda: self.history_down())
        ToolTip(next_button, "Next item in the input history")

        submit_button = widgetutils.make_button(frame_data, "Submit",
                                                lambda: self.submit(), right_padding=app.theme.right_padding)
        ToolTip(submit_button, "Send the prompt to the AI")

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
        text = config.inputs[self.history_index]
        self.set(text)

    def history_up(self) -> None:
        if not self.input.get():
            self.reset_history_index()

        if not config.inputs:
            return

        if self.history_index == -1:
            self.history_index = 0
        else:
            if self.history_index == len(config.inputs) - 1:
                self.clear()
                return
            else:
                self.history_index = (self.history_index + 1) % len(config.inputs)

        self.apply_history()

    def history_down(self) -> None:
        if not config.inputs:
            return

        if self.history_index == -1:
            self.history_index = len(config.inputs) - 1
        else:
            if self.history_index == 0:
                self.clear()
                return
            else:
                self.history_index = (self.history_index - 1) % len(config.inputs)

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

    def submit(self, tab_id: str = "", text: str = "") -> None:
        from .model import model
        from .display import display
        from . import filemanager

        if args.display:
            if not text:
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
            filemanager.add_input(text)

            if args.commands:
                if commands.exec(text):
                    return

            if tab.mode == "ignore":
                return

            display.to_bottom()

            if model.model_loading:
                return

            self.add_words(text)
            model.stream(text, tab.tab_id)
        else:
            display.toggle_scroll()

    def setup(self) -> None:
        path = paths.autocomplete

        if path.exists() and path.is_file():
            with open(path, "r", encoding="utf-8") as file:
                try:
                    self.autocomplete = json.load(file)
                except BaseException:
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
            if len(word) < args.input_memory_min:
                continue

            if word not in self.autocomplete:
                self.autocomplete.append(word)
                terminal.add_word(word)
                added = True

        if added:
            filemanager.save(paths.autocomplete, self.autocomplete)

    def show_textbox(self) -> None:
        def action(ans: str) -> None:
            self.submit(text=ans)

        text = self.input.get().strip()
        self.clear()
        Dialog.show_textbox("Write an input", lambda a: action(a), value=text)

    def input_command(self, arg: str) -> None:
        if arg:
            self.submit(text=arg)
        else:
            self.show_textbox()


inputcontrol = InputControl()
