from typing import AnyStr, Optional


class Bounding:
    def __init__(self, left=0, bottom=0, right=0, top=0):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    def get_wider_bounding(self, additional_size: Optional[int] = 1):
        return Bounding(self.left - additional_size, self.bottom - additional_size, self.right + additional_size,
                        self.top + additional_size)

    def __str__(self) -> AnyStr:
        return '{"left": ' + str(self.left) + \
               ', "right": ' + str(self.right) + \
               ', "top": ' + str(self.top) + \
               ', "bottom": ' + str(self.bottom) + '}'
