# Standard
from typing import Any, Dict, List

# Modules
from .app import app


class ArgSpec:
    def __init__(self) -> None:
        self.title = app.manifest["title"]
        self.version = app.manifest["version"]
        self.vinfo = f"{self.title} {self.version}"
        self.defaults: Dict[str, Any] = {}
        self.arguments: Dict[str, Any] = {}
        self.infos: List[str] = []

        self.add_arguments()

    def add_argument(self, key: str, info: str, **kwargs: Any) -> None:
        if key in self.arguments:
            raise Exception(f"Duplicate argument: {key}")

        if not info:
            raise Exception(f"Missing info for argument: {key}")

        if info in self.infos:
            raise Exception(f"Duplicate info for argument: {key}")

        self.arguments[key] = {
            "help": info,
            **kwargs,
        }

        self.infos.append(info)

    def add_arguments(self) -> None:
        self.add_argument(
            "version",
            action="version",
            info="Check the version of the program",
            version=self.vinfo,
        )

        self.add_argument(
            "no_tooltips",
            action="store_false",
            info="Don't show tooltips",
        )

        self.add_argument(
            "no_scrollbars",
            action="store_false",
            info="Don't show scrollbars",
        )

        self.add_argument(
            "no_colors",
            action="store_false",
            info="Don't show user colors",
        )

        self.add_argument(
            "no_avatars",
            action="store_false",
            info="Don't show user avatars",
        )

        self.add_argument(
            "no_system",
            action="store_false",
            info="Don't show system monitors",
        )

        self.add_argument(
            "no_system_colors",
            action="store_false",
            info="Disable system monitor colors",
        )

        self.add_argument(
            "no_cpu",
            action="store_false",
            info="Don't show the CPU monitor",
        )

        self.add_argument(
            "no_gpu",
            action="store_false",
            info="Don't show the GPU monitor",
        )

        self.add_argument(
            "no_gpu_ram",
            action="store_false",
            info="Don't show the GPU memory monitor",
        )

        self.add_argument(
            "no_gpu_temp",
            action="store_false",
            info="Don't show the GPU temperature monitor",
        )

        self.add_argument(
            "no_ram",
            action="store_false",
            info="Don't show the RAM monitor",
        )

        self.add_argument(
            "no_temp",
            action="store_false",
            info="Don't show the temperature monitor",
        )

        self.add_argument(
            "no_keyboard",
            action="store_false",
            info="Disable keyboard shortcuts",
        )

        self.add_argument(
            "no_taps",
            action="store_false",
            info="Disable double ctrl taps",
        )

        self.add_argument(
            "no_wrap",
            action="store_false",
            info="Disable wrapping when selecting items",
        )

        self.add_argument(
            "no_tabs",
            action="store_false",
            info="Don't show the tab bar",
        )

        self.add_argument(
            "no_stream",
            action="store_false",
            info="Don't stream responses",
        )

        self.add_argument(
            "no_empty",
            action="store_false",
            info="Don't save empty conversations",
        )

        self.add_argument(
            "no_bottom",
            action="store_false",
            info="Don't show the Bottom button",
        )

        self.add_argument(
            "no_bottom_autohide",
            action="store_false",
            info="Don't autohide the Bottom button",
        )

        self.add_argument(
            "no_reorder",
            action="store_false",
            info="Disable tab reordering by dragging",
        )

        self.add_argument(
            "no_tab_highlight",
            action="store_false",
            info="Don't highlight the tab when streaming",
        )

        self.add_argument(
            "no_commands",
            action="store_false",
            info="Disable commands when typing on the input",
        )

        self.add_argument(
            "no_intro",
            action="store_false",
            info="Don't print the intro in conversations",
        )

        self.add_argument(
            "no_terminal",
            action="store_false",
            info="Don't enable the interactive terminal",
        )

        self.add_argument(
            "no_clean_slate",
            action="store_false",
            info="Don't make a new tab when starting with an input",
        )

        self.add_argument(
            "no_more_button",
            action="store_false",
            info="Don't show the More button",
        )

        self.add_argument(
            "no_model_icon",
            action="store_false",
            info="Don't show the model icon",
        )

        self.add_argument(
            "no_model_feedback",
            action="store_false",
            info="Don't show model feedback when loading",
        )

        self.add_argument(
            "no_log_feedback",
            action="store_false",
            info="Don't show feedback when saving logs",
        )

        self.add_argument(
            "no_emojis",
            action="store_false",
            info="Don't use emojis",
        )

        self.add_argument(
            "no_input_memory",
            action="store_false",
            info="Don't remember input words",
        )

        self.add_argument(
            "no_write_button",
            action="store_false",
            info="Don't show the textbox button",
        )

        self.add_argument(
            "no_wrap_textbox",
            action="store_false",
            info="Don't wrap the textbox text",
        )

        self.add_argument(
            "no_markdown_snippets",
            action="store_false",
            info="Don't do snippet markdown",
        )

        self.add_argument(
            "no_markdown_italic",
            action="store_false",
            info="Don't do italic markdown",
        )

        self.add_argument(
            "no_markdown_bold",
            action="store_false",
            info="Don't do bold markdown",
        )

        self.add_argument(
            "no_markdown_highlights",
            action="store_false",
            info="Don't do highlight markdown",
        )

        self.add_argument(
            "no_markdown_urls",
            action="store_false",
            info="Don't do URL markdown",
        )

        self.add_argument(
            "no_log_errors",
            action="store_false",
            info="Don't log error messages to a file",
        )

        self.add_argument(
            "no_time",
            action="store_false",
            info="Don't show the loading time at startup",
        )

        self.add_argument(
            "no_gestures",
            action="store_false",
            info="Don't enable mouse gestures",
        )

        self.add_argument(
            "no_increment_logs",
            action="store_false",
            info="Always use the file name, don't increment with numbers",
        )

        self.add_argument(
            "no_confirm_urls",
            action="store_false",
            info="No need to confirm when opening URLs",
        )

        self.add_argument(
            "no_confirm_search",
            action="store_false",
            info="No need to confirm when searching",
        )

        self.add_argument(
            "no_confirm_close",
            action="store_false",
            info="No need to confirm closing tabs",
        )

        self.add_argument(
            "no_confirm_clear",
            action="store_false",
            info="No need to confirm clearing conversations",
        )

        self.add_argument(
            "no_fill_prompt",
            action="store_false",
            info="Don't fill the text input prompt in some cases when empty",
        )

        self.add_argument(
            "no_drag_and_drop",
            action="store_false",
            info="Don't enable drag and drop",
        )

        self.add_argument(
            "no_keywords",
            action="store_false",
            info="Don't do keyword replacements like ((now))",
        )

        self.add_argument(
            "no_prevnext",
            action="store_false",
            info="Don't show the Prev and Next buttons",
        )

        self.add_argument(
            "no_auto_name",
            action="store_false",
            info="Don't auto-name tabs based on input",
        )

        self.add_argument(
            "no_tab_double_click",
            action="store_false",
            info="Open new tabs on double click",
        )

        self.add_argument(
            "no_labels",
            action="store_false",
            info="Don't show the labels",
        )

        self.add_argument(
            "no_syntax_highlighting",
            action="store_false",
            info="Don't apply syntax highlighting to snippets",
        )

        self.add_argument(
            "test",
            action="store_true",
            info="Make a test tab for debugging",
        )

        self.add_argument(
            "only_text",
            action="store_true",
            info="Only show the text output. This is a preset that sets other arguments",
        )

        self.add_argument(
            "compact",
            action="store_true",
            info="Start in compact mode",
        )

        self.add_argument(
            "no_exit",
            action="store_true",
            info="Disable exit commands",
        )

        self.add_argument(
            "force",
            action="store_true",
            info="Allow opening multiple instances",
        )

        self.add_argument(
            "confirm_exit",
            action="store_true",
            info="Show confirm exit dialog",
        )

        self.add_argument(
            "compact_model",
            action="store_true",
            info="Hide the model frame in compact mode",
        )

        self.add_argument(
            "compact_system",
            action="store_true",
            info="Hide the system frame in compact mode",
        )

        self.add_argument(
            "compact_details_1",
            action="store_true",
            info="Hide the first details frame in compact mode",
        )

        self.add_argument(
            "compact_details_2",
            action="store_true",
            info="Hide the second details frame in compact mode",
        )

        self.add_argument(
            "compact_buttons",
            action="store_true",
            info="Hide the buttons frame in compact mode",
        )

        self.add_argument(
            "compact_file",
            action="store_true",
            info="Hide the URL frame in compact mode",
        )

        self.add_argument(
            "compact_input",
            action="store_true",
            info="Hide the input frame in compact mode",
        )

        self.add_argument(
            "maximize",
            action="store_true",
            info="Maximize the window on start",
        )

        self.add_argument(
            "numbers",
            action="store_true",
            info="Show numbers in the tab bar",
        )

        self.add_argument(
            "alt_palette",
            action="store_true",
            info="Show commands instead of descriptions in the palette",
        )

        self.add_argument(
            "terminal_vi",
            action="store_true",
            info="Use vi mode in the terminal",
        )

        self.add_argument(
            "tabs_always",
            action="store_true",
            info="Always show the tab bar even if only one tab",
        )

        self.add_argument(
            "verbose",
            action="store_true",
            info="Make the model verbose when streaming",
        )

        self.add_argument(
            "quiet",
            action="store_true",
            info="Don't show some messages",
        )

        self.add_argument(
            "debug",
            action="store_true",
            info="Show some information for debugging",
        )

        self.add_argument(
            "display",
            action="store_true",
            info="Only show the output and tabs",
        )

        self.add_argument(
            "listener",
            action="store_true",
            info="Listen for changes to the stdin file",
        )

        self.add_argument(
            "sticky",
            action="store_true",
            info="Make the window always on top",
        )

        self.add_argument(
            "avatars_in_logs",
            action="store_true",
            info="Show avatars in text logs",
        )

        self.add_argument(
            "short_labels",
            action="store_true",
            info="Use the short version of labels",
        )

        self.add_argument(
            "short_buttons",
            action="store_true",
            info="Use the short version of buttons",
        )

        self.add_argument(
            "short_system",
            action="store_true",
            info="Use the short version of system monitors",
        )

        self.add_argument(
            "errors",
            action="store_true",
            info="Show error messages",
        )

        self.add_argument(
            "terminal_height",
            type=int,
            info="Reserve these number of rows for the terminal",
        )

        self.add_argument(
            "width",
            type=int,
            info="Width of the window",
        )

        self.add_argument(
            "height",
            type=int,
            info="Height of the window",
        )

        self.add_argument(
            "max_tabs",
            type=int,
            info="Max number fo tabs to keep open",
        )

        self.add_argument(
            "max_tab_width",
            type=int,
            info="Max number of characters to show in a tab name",
        )

        self.add_argument(
            "config",
            type=str,
            info="Name or path of a config file to use",
        )

        self.add_argument(
            "session",
            type=str,
            info="Name or path of a session file to use",
        )

        self.add_argument(
            "on_log",
            type=str,
            info="Command to execute when saving any log file",
        )

        self.add_argument(
            "on_log_text",
            type=str,
            info="Command to execute when saving a text log file",
        )

        self.add_argument(
            "on_log_json",
            type=str,
            info="Command to execute when saving a JSON log file",
        )

        self.add_argument(
            "f1",
            type=str,
            info="Command to assign to the F1 key",
        )

        self.add_argument(
            "f2",
            type=str,
            info="Command to assign to the F2 key",
        )

        self.add_argument(
            "f3",
            type=str,
            info="Command to assign to the F3 key",
        )

        self.add_argument(
            "f4",
            type=str,
            info="Command to assign to the F4 key",
        )

        self.add_argument(
            "f5",
            type=str,
            info="Command to assign to the F5 key",
        )

        self.add_argument(
            "f6",
            type=str,
            info="Command to assign to the F6 key",
        )

        self.add_argument(
            "f7",
            type=str,
            info="Command to assign to the F7 key",
        )

        self.add_argument(
            "f8",
            type=str,
            info="Command to assign to the F8 key",
        )

        self.add_argument(
            "f9",
            type=str,
            info="Command to assign to the F9 key",
        )

        self.add_argument(
            "f10",
            type=str,
            info="Command to assign to the F10 key",
        )

        self.add_argument(
            "f11",
            type=str,
            info="Command to assign to the F11 key",
        )

        self.add_argument(
            "f12",
            type=str,
            info="Command to assign to the F12 key",
        )

        self.add_argument(
            "input",
            type=str,
            info="Prompt the AI automatically with this input when starting the program",
        )

        self.add_argument(
            "alias",
            type=str,
            action="append",
            info="Define an alias to run commands",
        )

        self.add_argument(
            "task",
            type=str,
            action="append",
            info="Define a task to run periodically",
        )

        self.add_argument(
            "gesture_threshold",
            type=str,
            info="Threshold in pixels for mouse gestures",
        )

        self.add_argument(
            "scroll_lines",
            type=int,
            info="How many lines to scroll the output",
        )

        self.add_argument(
            "auto_name_length",
            type=int,
            info="Max char length for auto tab names",
        )

        self.add_argument(
            "old_tabs_minutes",
            type=int,
            info="Consider a tab old after these minutes (using last modified date)",
        )

        self.add_argument(
            "max_list_items",
            type=int,
            info="Max number of items in context menu lists",
        )

        self.add_argument(
            "list_item_width",
            type=int,
            info="Max characters for the text of list items",
        )

        self.add_argument(
            "drag_threshold",
            type=int,
            info="The higher the number the less sensitive the tab dragging will be",
        )

        self.add_argument(
            "delay",
            type=float,
            info="Delay in seconds between each print when streaming",
        )

        self.add_argument(
            "prefix",
            type=str,
            info="Character used to prefix commands like /",
        )

        self.add_argument(
            "andchar",
            type=str,
            info="Character used to join commands like &",
        )

        self.add_argument(
            "system_threshold",
            type=int,
            info="Show system monitors as critical after this percentage threshold",
        )

        self.add_argument(
            "system_delay",
            type=int,
            info="Delay in seconds for system monitor updates",
        )

        self.add_argument(
            "autorun",
            type=str,
            info="Run this command at startup",
        )

        self.add_argument(
            "input_memory_min",
            type=int,
            info="Minimum number of characters for input words to be remembered",
        )

        self.add_argument(
            "listener_delay",
            type=float,
            info="Delay for the listener checks",
        )

        self.add_argument(
            "commandoc",
            type=str,
            info="Make the commandoc and save it on this path",
        )

        self.add_argument(
            "argumentdoc",
            type=str,
            info="Make the argument and save it on this path",
        )

        self.add_argument(
            "after_stream",
            type=str,
            info="Execute this command after streaming a response",
        )

        self.add_argument(
            "markdown",
            type=str,
            choices=["user", "ai", "all", "none"],
            info="Define where to apply markdown formatting",
        )

        self.add_argument(
            "browser",
            type=str,
            info="Open links with this browser",
        )

        self.add_argument(
            "font_diff",
            type=int,
            info="Add or subtract this from font sizes",
        )

        self.add_argument(
            "task_manager",
            type=str,
            info="Which task manager to use",
        )

        self.add_argument(
            "task_manager_gpu",
            type=str,
            info="Which task manager to use on the gpu monitors",
        )

        self.add_argument(
            "terminal",
            type=str,
            info="Which terminal to use",
        )

        self.add_argument(
            "progtext",
            type=str,
            info="Use this program as default for the progtext command",
        )

        self.add_argument(
            "progjson",
            type=str,
            info="Use this program as default for the progjson command",
        )

        self.add_argument(
            "program",
            type=str,
            info="Use this program as default for the progtext and progjson commands",
        )

        self.add_argument(
            "user_color",
            type=str,
            info="The color of the text for the name of the user",
        )

        self.add_argument(
            "ai_color",
            type=str,
            info="The color of the text for the name of the AI",
        )

        self.add_argument(
            "snippets_font",
            type=str,
            info="The font to use in snippets",
        )

        self.add_argument(
            "emoji_unloaded",
            type=str,
            info="Emoji to show when a model is not loaded",
        )

        self.add_argument(
            "emoji_local",
            type=str,
            info="Emoji to show when a model is loaded locally",
        )

        self.add_argument(
            "emoji_remote",
            type=str,
            info="Emoji to show when a model is loaded remotely",
        )

        self.add_argument(
            "emoji_loading",
            type=str,
            info="Emoji to show when loading a model",
        )

        self.add_argument(
            "emoji_storage",
            type=str,
            info="Emoji to show when saving a log",
        )

        self.add_argument(
            "name_mode",
            type=str,
            choices=["random", "noun", "empty"],
            info="What mode to use when naming new tabs",
        )

        self.add_argument(
            "arrow_mode",
            type=str,
            choices=["history", "scroll"],
            info="What to do on up and down arrows",
        )


argspec = ArgSpec()
