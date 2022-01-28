from numbers import Number
from typing import Iterable, Union

OptionItem = Union[str, Number]
Option = Union[OptionItem, Iterable[OptionItem]]