# Modules
from .config import config
from .widgets import widgets
from . import timeutils
from . import state

# Libraries
from llama_cpp import Llama  # type: ignore

# Standard
import threading
from pathlib import Path
from typing import List, Dict, Optional


class ContextList:
    def __init__(self) -> None:
        self.items: List[Dict[str, str]] = []

    def add(self, context_dict: Dict[str, str]) -> None:
        self.items.append(context_dict)
        self.limit()

    def limit(self) -> None:
        if config.context:
            self.items = self.items[-config.context:]
        else:
            self.reset()

    def reset(self) -> None:
        self.items = []


class Model:
    def __init__(self) -> None:
        self.mode = None
        self.lock = threading.Lock()
        self.stop_stream_thread = threading.Event()
        self.stream_thread = threading.Thread()
        self.contexts: Dict[str, ContextList] = {}
        self.streaming = False
        self.stream_loading = False
        self.model: Optional[Llama] = None
        self.model_loading = False
        self.loaded_model = ""
        self.loaded_format = ""
        self.load_thread = threading.Thread()
        self.stream_date = 0.0

    def unload(self, announce: bool = False) -> None:
        self.stop_stream()

        if self.model:
            self.model = None
            self.loaded_model = ""
            self.loaded_format = ""

            if announce:
                widgets.display.print("\n👻 Model unloaded")

    def load(self, prompt: str = "", output_id: str = "") -> None:
        if not config.model:
            return

        if self.is_loading():
            print("(Load) Slow down!")
            return

        model_path = Path(config.model)

        if not output_id:
            output_id = widgets.display.current_output

        if (not model_path.exists()) or (not model_path.is_file()):
            widgets.display.print("Error: Model not found. Check the path.", output_id=output_id)
            return

        def wrapper() -> None:
            self.do_load(config.model)

            if prompt:
                self.stream(prompt, output_id)

        self.unload()
        self.load_thread = threading.Thread(target=wrapper, args=())
        self.load_thread.daemon = True
        self.load_thread.start()

    def do_load(self, model: str) -> None:
        self.lock.acquire()
        self.model_loading = True

        now = timeutils.now()
        cformat = config.format

        try:
            fmt = config.format if (cformat != "auto") else None
            name = Path(model).name
            widgets.display.print(f"\n🫠 Loading {name}")
            widgets.update()

            self.model = Llama(
                model_path=str(model),
                chat_format=fmt,
                n_ctx=2048,
                verbose=False,
            )
        except BaseException as e:
            widgets.display.print("Error: Model failed to load.")
            self.model_loading = False
            print(e)
            return

        self.model_loading = False
        self.loaded_model = model
        self.loaded_format = cformat
        msg, now = timeutils.check_time("Model loaded", now)
        widgets.display.print(msg)
        self.lock.release()
        return

    def is_loading(self) -> bool:
        return self.model_loading or self.stream_loading

    def stop_stream(self) -> None:
        if self.stream_thread and self.stream_thread.is_alive():
            self.stop_stream_thread.set()
            self.stream_thread.join(timeout=3)
            self.stop_stream_thread.clear()
            widgets.display.print("\n* Interrupted *")

    def stream(self, prompt: str, output_id: str) -> None:
        if self.is_loading():
            print("(Stream) Slow down!")
            return

        if not self.model:
            self.load(prompt, output_id)
            return

        def wrapper(prompt: str, output_id: str) -> None:
            self.streaming = True
            self.do_stream(prompt, output_id)
            self.streaming = False

        self.stop_stream()
        self.stream_thread = threading.Thread(target=wrapper, args=(prompt, output_id))
        self.stream_thread.daemon = True
        self.stream_thread.start()

    def do_stream(self, prompt: str, output_id: str) -> None:
        self.lock.acquire()
        self.stream_loading = True

        widgets.show_model()
        prompt = prompt.strip()

        if not self.model:
            print("Model not loaded")
            return

        if not prompt:
            print("Empty prompt")
            return

        def replace_content(content: str) -> str:
            if config.name_user:
                content = content.replace("@name_user", config.name_user)

            if config.name_ai:
                content = content.replace("@name_ai", config.name_ai)

            return content

        widgets.prompt("user", output_id=output_id)
        widgets.display.insert(prompt, output_id=output_id)
        widgets.enable_stop_button()

        full_prompt = prompt

        if config.prepend:
            full_prompt = config.prepend + ". " + full_prompt

        if config.append:
            full_prompt = full_prompt + ". " + config.append

        context_list = self.contexts.get(output_id)

        if not context_list:
            context_list = ContextList()
            self.contexts[output_id] = context_list

        if config.context > 0:
            context_dict = {"user": full_prompt}
        else:
            context_dict = None

        system = replace_content(config.system)
        messages = [{"role": "system", "content": system}]

        if context_list.items:
            for item in context_list.items:
                for key in item:
                    content = item[key]

                    if key == "user":
                        content = replace_content(content)

                    messages.append({"role": key, "content": content})

        if config.printlogs:
            print("-----")
            print("prompt:", full_prompt)
            print("messages:", len(messages))
            print("context:", config.context)
            print("max_tokens:", config.max_tokens)
            print("temperature:", config.temperature)
            print("top_k:", config.top_k)
            print("top_p:", config.top_p)
            print("seed:", config.seed)

        content = full_prompt
        content = replace_content(content)
        messages.append({"role": "user", "content": content})

        added_name = False
        token_printed = False
        last_token = " "
        tokens = []

        state.add_model(config.model)
        state.add_system(config.system)
        state.add_prepends(config.prepend)
        state.add_appends(config.append)
        state.add_input(prompt)

        now = timeutils.now()
        self.stream_date = now

        try:
            output = self.model.create_chat_completion(
                stream=True,
                messages=messages,
                max_tokens=config.max_tokens,
                temperature=config.temperature,
                top_k=config.top_k,
                top_p=config.top_p,
                seed=config.seed,
            )
        except BaseException as e:
            print("Stream Error:", e)
            self.stream_loading = False
            return

        self.stream_loading = False

        if self.stream_date != now:
            return

        if self.stop_stream_thread.is_set():
            return

        try:
            for chunk in output:
                if self.stop_stream_thread.is_set():
                    break

                delta = chunk["choices"][0]["delta"]

                if "content" in delta:
                    if not added_name:
                        widgets.prompt("ai", output_id=output_id)
                        added_name = True

                    token = delta["content"]

                    if token == "\n":
                        if not token_printed:
                            continue
                    elif token == " ":
                        if last_token == " ":
                            continue

                    last_token = token

                    if not token_printed:
                        token = token.lstrip()
                        token_printed = True

                    tokens.append(token)
                    widgets.display.insert(token, output_id=output_id)
        except BaseException as e:
            print("Stream Read Error:", e)

        if context_dict and tokens:
            context_dict["assistant"] = "".join(tokens).strip()
            context_list.add(context_dict)

        self.lock.release()

    def clear_context(self, output_id: str) -> None:
        context_list = self.contexts.get(output_id)

        if context_list:
            context_list.reset()


model = Model()
