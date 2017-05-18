"""Here will be the dschictionary.py's description."""


__copyright__ = "Copyright (C) 2016, B. Zolt'n Gorza"


import enum
import dsch_entry as entry


"""The used language_separator within your dschictionary file (default: ->)."""
LANGUAGE_SEPARATOR = "->"


"""
These are the possible indentation characters.

It is hardly recommended to contain the DEFAULT_INDENT_CHAR (see below).
"""
INDENT_CHARS = ' \t_-.'


"""
It is the default indentation within your dschictionary (default: \t).

The indentation's level depends on the number of this character before the
meaning.
It should be " ", "\t", or "_".
If you choose another character, it may cause an error that's not handled.
"""
DEFAULT_INDENT_CHAR = " "


class ReadStates(enum.IntEnum):
    """This enum is for file reading, defines the current state."""

    Title = 0,
    Languages = 1,
    Dictionary = 2,
    Entry = 3,
    EoE = 4


class LanguageError(Exception):
    """
    Simple Error class for Language errors.

    It's raised when the program find a language-definition error in the
    dschictionary file.
    """

    expression = ""
    message = ("Error -- To define languages, this line should be in the "
               "following format: <language of entry> -> <language of "
               "definition>")

    def __init__(self, expression, message=None):
        """
        Just initialize it.

        :param expression: The expression that caused error
        :param message: The message for the user
        """
        Exception.__init__(self)
        self.expression = expression
        self.message = message if (message is not None) else self.message


class Dschictionary:
    """This class is contains our whole dictionary."""

    _title = ""
    _entries = []
    entry_language = ""
    definition_language = ""
    error = ""

    def __init__(self, title="", entrylang="", defilang=""):
        """
        Initialize a Dschictionary.

        Parameters:
            title -- Title
            entrylang -- Language of entries
            defilang -- Language of definitions
        """
        self.init(title, entrylang, defilang)

    def init(self, title: str, entrylang: str, defilang: str):
        """
        Initialize a Dschictionary.

        Parameters:
            title -- Title
            entrylang -- Language of entries
            defilang -- Language of definitions
        """
        self._title = title
        self.entry_language = entrylang
        self.definition_language = defilang
        self.error = ""
        self._entries = []

    def title(self) -> str:
        """It returns the dschictionary's title."""
        return self._title or "n/a"

    def entries(self) -> list:
        """It returns the entries as a list."""
        return self._entries or []

    def get_entries_as_string(self) -> str:
        """It returns all entries as a single string."""
        return "\n \n".join([str(e) for e in self.entries()])

    def num_of_entries(self) -> int:
        """It returns the number of entries."""
        return len(self._entries)

    def get_errors(self) -> str:
        """It returns the errors or a "no errors" message."""
        return self.error or "There's no errors :)"

    def __add__(self, entry_: entry.Entry):
        """It adds a single Entry instance."""
        self._entries.append(entry_)
        return self

    def _sort_entries(self):
        """It sorts the entries by word."""
        #ut.sort(key=lambda x: x.count, reverse=True)
        self._entries.sort(key=lambda e: e.word())

    def read_dschictionary(self, filename: str):
        """
        It reads a dschictionary from a file and process its content.

        Parameters:
            filename -- The dschictionary file's name
        """
        idx = 1  # don't start to count from 0! That would not work (don't ask)

        # Starting the process
        state = ReadStates.Title
        self._title = ".".join(filename.split(".")[:len(self._title)-1])

        # Trying to open the file
        try:
            file = open(filename, 'r')
        except FileNotFoundError as fnfe:
            self.error = "{0} -- {1}".format(fnfe.filename, fnfe.strerror)
            return self

        # Reading the languages
        state = ReadStates.Languages
        line = file.readline()
        try:
            if LANGUAGE_SEPARATOR in line:
                tmp = line.split(LANGUAGE_SEPARATOR)
                if len(tmp) == 2:  # if both of needed languages are defined
                    self.entry_language = tmp[0].strip()
                    self.definition_language = tmp[1].strip()
                else:
                    raise LanguageError(line)
            else:
                raise LanguageError(line)
        except LanguageError as langerror:
            self.error = "{0}\nYour file contains this: {1}".format(
                langerror.message,
                langerror.expression
            )
        except Exception as exc:
            self.error = (
                "Gotta catch 'em all! "
                "We don't know what is the problem, "
                "but it is about your language definition or "
                "where it should to be.\n"
                "Here is the Python's own thing about it: "
            ) + exc.args

        # Reading the dschictionary
        state = ReadStates.Dictionary
        tmpe = file.readline()  # not needed, but better than 2 lines of this
        for line in file:
            # trim the unwanted characters (except the indent char)
            line = line.strip(INDENT_CHARS.replace(DEFAULT_INDENT_CHAR,
                                                   '') + '\n')
            if line:  # if the line isn't empty (after the trim)
                if state == ReadStates.Entry:  # if the entry is under reading
                    tmpe.add_entry_part(line, DEFAULT_INDENT_CHAR)
                else:  # if it'll be a new entry
                    tmpe = entry.Entry(idx)  # add id and word
                    tmpe.add_word(line)
                    idx += 1
                    state = ReadStates.Entry
            else:  # if the line is empty (probably between two entries)
                self += tmpe
                tmpe = None
                state = ReadStates.EoE
        if tmpe:
            self += tmpe

        # Closing the file and handle the possible errors
        file.close()
        if state == ReadStates.Dictionary:
            self.error = (
                "The dschictionary doesn't contain any data except "
                "the language definitions."
            )

        self._sort_entries()  # Sorting entries alphabetically

        return self

    @staticmethod
    def create_dschictionary(filename: str):
        """
        It is create and return a dschictionary and needs only a file name.

        Parameter:
            filename -- The dschictionary file's name

        Return:
            A full, processed dschictionary
        """
        return Dschictionary().read_dschictionary(filename)

    def __str__(self) -> str:
        """
        It returns the dschictionary's title, entry- and definition language.

        If not each of them are defined, it returns something --
        not implemented yet.
        """
        return (
            self._title +
            " (" +
            self.entry_language +
            " -> " +
            self.definition_language +
            ")"
        ) if (self._title and
              self.entry_language and
              self.definition_language) else ""


if __name__ == '__main__':
    dsch = Dschictionary.create_dschictionary("example.txt")
    print(str(dsch) or dsch.error)
    print(len(dsch.entries()))
    print(dsch.get_entries_as_string())
    print(dsch.get_errors())
