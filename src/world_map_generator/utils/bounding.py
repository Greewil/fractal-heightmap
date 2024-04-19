from __future__ import annotations

from typing import AnyStr, Optional, Callable


class Bounding:

    @classmethod
    def update_max_min(cls, x, y, bounding: Bounding):
        if x < bounding.left:
            bounding.left = x
        if x > bounding.right:
            bounding.right = x
        if y < bounding.bottom:
            bounding.bottom = y
        if y > bounding.top:
            bounding.top = y

    def __init__(self, left=0, bottom=0, right=0, top=0):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    def get_wider_bounding(self, additional_size: Optional[int] = 1):
        return Bounding(self.left - additional_size, self.bottom - additional_size, self.right + additional_size,
                        self.top + additional_size)

    def add_bounding(self, additional_values: Bounding) -> None:
        """
        Adds values of corresponding additional_values sides to the current bounding (left to left etc.).
        """
        self.left += additional_values.left
        self.right += additional_values.right
        self.top += additional_values.top
        self.bottom += additional_values.bottom

    def for_each(self, func: Callable[[int, int], None],
                 include_both_borders: Optional[int] = False):
        """ Runs functions for each point in bounding including points in left and top borders. """
        additional_value = 0
        if include_both_borders:
            additional_value = 1
        for x in range(self.left, self.right + additional_value):
            for y in range(self.bottom, self.top + additional_value):
                func(x, y)

    def __str__(self) -> AnyStr:
        return '{"left": ' + str(self.left) + \
               ', "right": ' + str(self.right) + \
               ', "top": ' + str(self.top) + \
               ', "bottom": ' + str(self.bottom) + '}'
