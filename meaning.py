"""Meaning class for Dschictionary."""


__copyright__ = "Copyright (C) 2016, B. Zolt'n Gorza"


import re
import pos


"""
This dictionary contains the short form's meaning, e.g.: n -> noun.

Modify it as you want (but it's recommended to keep the original version)
Original version is for a znacra -> english dictionary and a few other is
for general usage.
"""
PART_OF_SPEECH = pos.DEFAULT


class Meaning:
    """It a definition / meaning of a word."""

    _part_of_speech = ""
    _case = ""
    _class = ""
    _definition = ""
    _level = 0

    def __init__(self, pos="", case="", class_="", definition="", level=0):
        """
        Initializing a Meaning with 0 or more basic arguments.

        Parameters:
            pos -- Meaning's part-of-speech
            case -- Meaning's case
            class -- Meaning's class that it belongs to
            definition -- Meaning's definition
            level -- Meaning's level
        """
        #if pos in PART_OF_SPEECH:
        #    pos = PART_OF_SPEECH[pos]
        self._part_of_speech = pos
        self._case = case
        self._class = class_
        self._definition = definition
        self._level = level

    def add_part_of_speech(self, nu_pos: str):
        """Add or modify the part of speech."""
        #if nu_pos in PART_OF_SPEECH:
        #    nu_pos = PART_OF_SPEECH[nu_pos]
        self._part_of_speech = nu_pos

    def add_case(self, nu_case: str):
        """Add or modify case."""
        self._case = nu_case

    def add_class(self, nu_class: str):
        """Add or modify class."""
        self._class = nu_class

    def add_definition(self, nu_definition: str):
        """Add or modify definition."""
        self._definition = nu_definition

    def add_level(self, nu_level: int):
        """Add or modify level."""
        self._level = nu_level

    def part_of_speech(self) -> str:
        """Get the part of speech."""
        return self._part_of_speech

    def case(self) -> str:
        """Get case."""
        return self._case

    def class_(self) -> str:
        """Get class."""
        return self._class

    def definition(self) -> str:
        """Get definition."""
        return self._definition or "n/a"

    def level(self) -> int:
        """Get level."""
        return self._level

    def get_meaning_as_dict(self) -> dict:
        """It returns a meaning as dict (keys: pos, cas, cls, def, lvl)."""
        return {'pos': self.part_of_speech(),
                'cas': self.case(),
                'cls': self.class_(),
                'def': self.definition(),
                'lvl': self.level()}

    def __str__(self):
        """Return a wannabe well-formated string."""
        return ("pos: {pos}, "
                "case: {case}, "
                "class: {cls}, "
                "definition: {def_}, "
                "lvl: {lvl}").format(pos=self.part_of_speech(),
                                     case=self.case(),
                                     cls=self.class_(),
                                     def_=self.definition(),
                                     lvl=self.level())

    @staticmethod
    def is_meaning(text: str, indentchar: str) -> tuple:
        """
        It tests a string it can or cannot be a meaning.

        Parameters:
            text -- the text to be checked
            indentchar -- the character of indentation

        Return:
            If 'text' defines a new Meaning, it returns a tuple with the next
            arguments: (pos, case, class, definition, level). It can be
            directly used for the static 'create_meaning' and for the
            Meaning's constructor.
            Otherwise it returns None.
        """
        match = re.fullmatch(indentchar + r"*(\(\w*\+?\w*:?\w*\))?.*",
                             text)

        # if 'text' is a valid meaning
        if match:
            all_ = re.search((r"(?P<lvl>[" + indentchar + r"]*)"
                              r"\((?P<pos>[\w]*)\+?(?P<case>[\w]*)"
                              r":?(?P<cls>[\w]*)\)(?P<def>[\w'\" ,\.]*)"),
                             text)
            all_ = all_.groupdict() if all_ else None
        else:
            return

        return (all_['pos'].strip(),
                all_['case'].strip(),
                all_['cls'].strip(),
                all_['def'].strip(),
                len(all_['lvl'])) if all_ else None

    @staticmethod
    def create_meaning(pos, case, class_, definition, level):
        """
        It creates and returns a Meaning instance.

        It's practically equal to Meaning().

        Parameters:
            pos -- Meaning's part-of-speech
            case -- Meaning's case
            class -- Meaning's class that it belongs to
            definition -- Meaning's definition
            level -- Meaning's level

        Return:
            A new Meaning instance
        """
        return Meaning(pos, case, class_, definition, level)
