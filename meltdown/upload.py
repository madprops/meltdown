from __future__ import annotations

# Modules
from .app import app
from .utils import utils
from .config import config
from .display import display
from .rentry import Rentry
from .dialogs import Dialog, Commands
from .args import args
from . import formats


class Upload:
    def upload(self, tab_id: str | None = None, mode: str = "") -> None:
        messages = display.has_messages()
        ignored = display.is_ignored()

        if (not messages) or ignored:
            return

        if mode in ["last", "all"]:
            self.do_upload(tab_id, mode)
            return

        def action(mode: str) -> None:
            Dialog.hide_all()
            app.update()
            self.do_upload(tab_id, mode)

        cmds = Commands()
        cmds.add("Last Item", lambda a: action("last"))
        cmds.add("All Of It", lambda a: action("all"))

        Dialog.show_dialog(
            f"Upload conversation to\n{config.rentry_site}", commands=cmds
        )

    def after_upload(self, url: str, password: str, tab_id: str) -> None:
        display.print(
            f"Uploaded: {url} ({password})",
            do_format=True,
            tab_id=tab_id,
        )

        def copy_url() -> None:
            utils.copy(url)

        def copy_all() -> None:
            utils.copy(f"{url} ({password})")

        cmds = Commands()
        cmds.add("Copy All", lambda a: copy_all())
        cmds.add("Copy URL", lambda a: copy_url())

        Dialog.show_dialog(f"{url} ({password})", commands=cmds)

    def do_upload(self, tab_id: str | None = None, mode: str = "all") -> None:
        if not tab_id:
            tab_id = display.current_tab

        tabconvo = display.get_tab_convo(tab_id)

        if not tabconvo:
            return

        if not tabconvo.convo.items:
            return

        text = formats.get_markdown(tabconvo.convo, mode=mode, name_mode="upload")

        if args.upload_password:
            password = args.upload_password
        else:
            password = utils.random_word()

        try:
            Rentry(
                text=text,
                password=password,
                tab_id=tab_id,
                after_upload=self.after_upload,
            )
        except Exception as e:
            utils.error(e)


upload = Upload()
