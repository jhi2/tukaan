from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any, Optional

if sys.version_info >= (3, 9):
    from collections.abc import Callable
    from typing import Protocol
else:
    from typing import Callable
    from typing_extensions import Protocol

from tukaan._tcl import Procedure, Tcl
from tukaan._typing import P, T, T_co, T_contra

if TYPE_CHECKING:
    from tukaan._base import TkWidget


def cget(widget: TkWidget, return_type: T | type[T], option: str) -> T:
    return Tcl.call(return_type, widget, "cget", option)


def config(widget: TkWidget, **kwargs: Any) -> None:
    assert len(kwargs) == 1

    [(key, value)] = kwargs.items()
    Tcl.call(None, widget, "configure", f"-{key}", value if value is not None else "")


class RWProperty(Protocol[T_co, T_contra]):
    def __get__(self, instance: TkWidget, owner: object = None) -> T_co:
        ...

    def __set__(self, instance: TkWidget, value: T_contra) -> None:
        ...


class OptionDescriptor(RWProperty[T, T_contra]):
    def __init__(self, option: str, type_: type[T]) -> None:
        self._option = option
        self._type = type_

    def __get__(self, instance: TkWidget, owner: object = None) -> T:
        if owner is None:
            return NotImplemented
        return cget(instance, self._type, f"-{self._option}")

    def __set__(self, instance: TkWidget, value: T_contra) -> None:
        config(instance, **{self._option: value})


class DynamicProperty:
    def __set_name__(self, owner: type[TkWidget], name: str) -> None:
        if not self._option:
            self._option = name


class IntDescriptor(OptionDescriptor[int, int], DynamicProperty):
    def __init__(self, option: str = "") -> None:
        super().__init__(option, int)


class FloatDescriptor(OptionDescriptor[float, float], DynamicProperty):
    def __init__(self, option: str = "") -> None:
        super().__init__(option, float)


class BoolDescriptor(OptionDescriptor[bool, bool], DynamicProperty):
    def __init__(self, option: str = "") -> None:
        super().__init__(option, bool)


class StrDescriptor(OptionDescriptor[str, str], DynamicProperty):
    def __init__(self, option: str = "") -> None:
        super().__init__(option, str)


class FocusableProp(BoolDescriptor):
    def __init__(self) -> None:
        super().__init__("takefocus")

    def __get__(self, instance: TkWidget, owner: object = None) -> T:
        if owner is None:
            return NotImplemented
        result = Tcl.call(str, instance, "cget", "-takefocus")
        if result == "ttk::takefocus":
            return Tcl.call(bool, "ttk::takefocus", instance)
        return Tcl.from_(bool, result)


class ActionProp(OptionDescriptor[Procedure, Optional[Callable[P, T]]]):
    def __init__(self, option: str = "command") -> None:
        super().__init__(option, Procedure)
