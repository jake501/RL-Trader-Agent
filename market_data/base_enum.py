from enum import Enum, EnumMeta

"""
Base Enum created that allows all other enums in this module to extend from. I added this to allow code to use list on
the enum to return a list of the values available.
"""


class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class BaseEnum(Enum, metaclass=MetaEnum):
    pass


