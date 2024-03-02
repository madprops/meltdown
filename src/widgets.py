# Modules
from config import config
import widgetutils
from framedata import FrameData

# Standard
import tkinter as tk
from typing import Any
from tkinter import filedialog


class Widgets:
    def __init__(self) -> None:
        def get_d() -> FrameData:
            return FrameData(widgetutils.make_frame(), 0)

        # Model
        d = get_d()
        d.frame.grid_columnconfigure(1, weight=1)
        widgetutils.make_label(d, "Model")
        self.model = widgetutils.make_input(d, sticky="ew")
        widgetutils.make_button(d, "Browse", lambda: self.browse_model())
        widgetutils.make_button(d, "Menu", lambda: self.show_main_menu())

        # Settings
        d = get_d()
        widgetutils.make_label(d, "Name 1")
        self.name_1 = widgetutils.make_input(d)
        widgetutils.make_label(d, "Name 2")
        self.name_2 = widgetutils.make_input(d)
        widgetutils.make_label(d, "Tokens")
        self.max_tokens = widgetutils.make_input(d)
        widgetutils.make_label(d, "Temp")
        self.temperature = widgetutils.make_input(d)

        # System
        d = get_d()
        d.frame.grid_columnconfigure(1, weight=1)
        widgetutils.make_label(d, "System")
        self.system = widgetutils.make_input(d, sticky="ew")
        widgetutils.make_label(d, "Top K")
        self.top_k = widgetutils.make_input(d)
        widgetutils.make_label(d, "Top P")
        self.top_p = widgetutils.make_input(d)

        # Output
        d = get_d()
        d.frame.grid_columnconfigure(0, weight=1)
        d.frame.grid_rowconfigure(0, weight=1)
        self.output = widgetutils.make_text(d, state="disabled", sticky="nsew")

        # Input
        d = get_d()
        d.frame.grid_columnconfigure(1, weight=1)
        widgetutils.make_label(d, "Prompt")
        self.input = widgetutils.make_input(d, sticky="ew")
        widgetutils.make_label(d, "Context")
        values = [0, 1, 5, 10, 100]
        self.context = widgetutils.make_select(d, values)
        self.context.configure(width=5)
        widgetutils.make_button(d, "Submit", lambda: self.submit())

        self.output_menu = tk.Menu(config.app, tearoff=0, font=config.font)
        self.model_menu = tk.Menu(config.app, tearoff=0, font=config.font)
        self.main_menu = tk.Menu(config.app, tearoff=0, font=config.font)

    def fill(self) -> None:
        widgetutils.set_text(self.model, config.model)
        widgetutils.set_text(self.name_1, config.name_1)
        widgetutils.set_text(self.name_2, config.name_2)
        widgetutils.set_text(self.max_tokens, config.max_tokens)
        widgetutils.set_text(self.temperature, config.temperature)
        widgetutils.set_text(self.system, config.system)
        widgetutils.set_text(self.top_k, config.top_k)
        widgetutils.set_text(self.top_p, config.top_p)
        widgetutils.set_select(self.context, config.context)

    def setup(self) -> None:
        import state

        self.fill()

        self.model.bind("<Button-3>", lambda e: self.show_model_menu(e))
        self.model.bind("<Button-1>", lambda e: self.hide_menus())
        self.model.bind("<Button-1>", lambda e: self.hide_menus())

        self.output_menu.add_command(label="Clear", command=lambda: self.clear_output())
        self.output_menu.add_command(label="Select All", command=lambda: widgetutils.select_all(self.output))
        self.output_menu.add_command(label="Copy All", command=lambda: widgetutils.copy_all(self.output))

        self.main_menu.add_command(label="Recent Models", command=lambda: self.show_model_menu(None))
        self.main_menu.add_command(label="Reset Config", command=lambda: state.reset_config())
        self.main_menu.add_command(label="Reset Models", command=lambda: state.reset_models())
        self.main_menu.add_command(label="Save Log", command=lambda: state.save_log())

        self.output.bind("<Button-3>", lambda e: self.show_output_menu(e))
        self.output.bind("<Button-1>", lambda e: self.hide_menus())
        self.output.bind("<Button-1>", lambda e: self.hide_menus())

        self.input.bind("<Return>", lambda e: self.submit())

        self.name_1.bind("<FocusOut>", lambda e: state.update_name_1())
        self.name_2.bind("<FocusOut>", lambda e: state.update_name_2())
        self.max_tokens.bind("<FocusOut>", lambda e: state.update_max_tokens())
        self.temperature.bind("<FocusOut>", lambda e: state.update_temperature())
        self.system.bind("<FocusOut>", lambda e: state.update_system())
        self.model.bind("<FocusOut>", lambda e: state.update_model())
        self.top_k.bind("<FocusOut>", lambda e: state.update_top_k())
        self.top_p.bind("<FocusOut>", lambda e: state.update_top_p())
        self.context.bind("<<ComboboxSelected>>", lambda e: state.update_context())

        self.input.focus_set()

    def print(self, text: str, linebreak: bool = True) -> None:
        if not widgetutils.exists():
            return

        left = ""
        right = ""

        if widgetutils.text_length(self.output) and \
                (widgetutils.last_character(self.output) != "\n"):
            left = "\n"

        if linebreak:
            right = "\n"

        text = left + text + right
        widgetutils.insert_text(self.output, text, True)
        widgetutils.to_bottom(self.output)

    def insert(self, text: str) -> None:
        if not widgetutils.exists():
            return

        widgetutils.insert_text(self.output, text, True)
        widgetutils.to_bottom(self.output)

    def show_output_menu(self, event: Any) -> None:
        self.output_menu.post(event.x_root, event.y_root)

    def hide_output_menu(self) -> None:
        self.output_menu.unpost()

    def show_model_menu(self, event: Any) -> None:
        import state

        self.model_menu.delete(0, tk.END)

        for model in config.models:
            def proc(model: str = model) -> None:
                self.set_model(model)

            self.model_menu.add_command(label=model, command=proc)

        if len(config.models):
            self.model_menu.add_separator()
            self.model_menu.add_command(label="Reset", command=lambda: state.reset_models())
        else:
            self.model_menu.add_command(label="Empty", command=lambda: state.models_info())

        if event:
            self.model_menu.post(event.x_root, event.y_root)
        else:
            widgetutils.show_menu_at_center(self.model_menu)

    def hide_model_menu(self) -> None:
        self.model_menu.unpost()

    def hide_menus(self) -> None:
        self.hide_output_menu()
        self.hide_model_menu()
        self.hide_main_menu()

    def browse_model(self) -> None:
        import state
        file = filedialog.askopenfilename(initialdir=state.get_models_dir())
        widgetutils.set_text(self.model, file)
        state.update_model()

    def submit(self) -> None:
        from model import model
        text = self.input.get()

        if text:
            self.clear_input()
            model.stream(text)

    def clear_output(self) -> None:
        widgetutils.clear_text(self.output, True)

    def clear_input(self) -> None:
        widgetutils.clear_text(self.input)

    def prompt(self, num: int) -> None:
        name = getattr(config, f"name_{num}")
        prompt = f"{name}: "
        self.print(prompt, False)

    def set_model(self, model: str) -> None:
        import state
        widgetutils.set_text(self.model, model)
        state.update_model()

    def intro(self) -> None:
        self.print("Welcome to Meltdown")
        self.print("Type a prompt and press Enter to continue")
        self.print("The specified model will load automatically")

    def show_model(self) -> None:
        widgetutils.set_text(self.model, config.model)

    def update(self) -> None:
        config.app.update_idletasks()

    def show_main_menu(self) -> None:
        widgetutils.show_menu_at_center(self.main_menu)

    def hide_main_menu(self) -> None:
        self.main_menu.unpost()


widgets: Widgets = Widgets()
