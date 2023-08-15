from os import get_terminal_size, system


class Helper():
    term_size = get_terminal_size().columns

    @classmethod
    def top_wrap(cls, string, char="*"):
        system("clear")
        cls.term_wrap(string, char)

    @classmethod
    def term_wrap(cls, string, char="*"):
        cls.star_line(char)
        cls.center_string_stars(string, char)
        cls.star_line(char)

    @classmethod
    def star_line(cls, char="*"):
        print(char * cls.term_size)

    @classmethod
    def center_string_stars(cls, string, char="*"):
        half_size = (cls.term_size - len(string) - 2) / 2
        half_stars = char * int(half_size)
        print(f"{half_stars} {string} {half_stars}")
