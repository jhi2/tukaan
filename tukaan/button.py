from typing import Callable, Optional

from ._base import BaseWidget, TkWidget


class Button(BaseWidget):
    _tcl_class = "ttk::button"
    _keys = {
        "on_click": ("func", "command"),
        "default": str,
        "focusable": (bool, "takefocus"),
        "style": str,
        "text": str,
        "underline": int,
        "width": int,
    }

    def __init__(
        self,
        parent: Optional[TkWidget] = None,
        on_click: Optional[Callable] = None,
        default: Optional[str] = None,
        focusable: Optional[bool] = None,
        style: Optional[str] = None,
        text: Optional[str] = None,
        underline: Optional[int] = None,
        width: Optional[int] = None,
    ) -> None:
        BaseWidget.__init__(
            self,
            parent,
            command=on_click,
            default=default,
            style=style,
            takefocus=focusable,
            width=width,
            underline=underline,
        )
        self.config(text=text)

    def invoke(self):
        self._tcl_call(None, self, "invoke")
