"""
Allows to print colored console text
"""
from colorama import (init, Fore) #, Back, Style)
init()


COLORS = {
    "red": Fore.RED,
    "blue": Fore.BLUE,
    "green": Fore.GREEN,
    "magenta": Fore.MAGENTA,
    "cyan": Fore.CYAN
}


class Rainbow:
    """
    Allows to print colored console text
    """
    @staticmethod
    def prent(color: str, *args):
        """
        Prints the output with a specific color
        """
        print(COLORS[color], *args, Fore.RESET)

    @staticmethod
    def color_me(color="yellow"):
        """
        Changes the font color from this line on
        """
        print(COLORS[color])

    @staticmethod
    def color_me_not():
        """
        Removes the current color
        """
        print(Fore.RESET)
