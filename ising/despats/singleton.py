#!/usr/bin/python3

"""
Represents a singleton.
"""


class Singleton:  # pylint: disable=too-few-public-methods
    """
Represents a singleton class.
"""

    __singletonptr = None

    @classmethod
    def getsingleton(cls):
        """
Gets the singleton instance.
"""
        if cls.__singletonptr is None:
            cls.__singletonptr = cls()
        return cls.__singletonptr
