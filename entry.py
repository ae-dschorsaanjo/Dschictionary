"""Entry class and for Dschictionary."""


__copyright__ = "Copyright (C) 2016, B. Zolt'n Gorza"


import meaning


"""Default value for empty entries."""
ENTRY_NO_ID = -1


class Entry:
    """
    Each instance of this class contains an entry of a dictionary.

    Because of it's a simple program, it can have only the basic informations,
    such as the word itself, its pronunciation and
    meanings.
    """

    _id = ""
    _word = ""
    _pronunciation = ""
    _description = ""
    _meanings = []
    _origin = ""  # <
    _comment = ""  # |
    _see = ""  # >

    ORIGIN_CHAR = "<"
    COMMENT_CHAR = "|"
    SEE_CHAR = ">"
    PRONOUNCIATION_CHAR = "/"

    def __init__(self,
                 id_=ENTRY_NO_ID,
                 word="",
                 pronunciation="",
                 description="",
                 meanings=[],
                 origin="",
                 comment="",
                 see=""):
        """
        Define a single Entry.

        Parameters:
            word -- The word that it's entry for
            pronunciation -- The word's pronunciation
            meanings -- It's a list of different meanings. The elements of the
                list must be Meaning instances!
            origin -- Word's origin
            comment -- Comment(s) about the word
        """
        self._id = id_
        self._word = word
        self._pronunciation = pronunciation
        self._description = description
        self._meanings = self._meaning_loop(meanings)
        self._origin = origin
        self._comment = comment
        self._see = see

    def _meaning_loop(self, meanings: list) -> list:
        """It adds multiple meanings."""
        out = []
        for meaning_ in meanings:
            if isinstance(meaning_, meaning_.Meaning):
                out.append(meaning_)
        return out

    def add_id(self, id_: int):
        """It adds or modify id."""
        if (self.id == ENTRY_NO_ID and
                id_ != ENTRY_NO_ID):
            self._id = id_

    def add_word(self, nu_word: str):
        """
        It adds or modify word and additionally pronounciation too.

        Parameters:
            nu_word -- the new word and pronounciation too if it's added
        """
        if self.PRONOUNCIATION_CHAR in nu_word:
            word, pro = nu_word.split(self.PRONOUNCIATION_CHAR, 1)
            self._word = word.strip()
            self._pronunciation = \
                pro.strip().rstrip(self.PRONOUNCIATION_CHAR).strip()
        else:
            self._word = nu_word

    def add_description(self, nu_description: str):
        """Add or modify description."""
        self._description = nu_description.strip()

    def _add_word_or_desc(self, nu_foo: str):
        """Add a word, or the word is given, add a description."""
        if self._word:
            self.add_description(nu_foo)
        else:
            self.add_word(nu_foo)

    def add_pronunciation(self, nu_pronunciation: str):
        """Add or modify description."""
        self._pronunciation = \
            nu_pronunciation.strip(self.PRONOUNCIATION_CHAR).strip()

    def add_meaning_via_fields(self,
                               pos: str,
                               case: str,
                               class_: str,
                               definition: str,
                               level: int):
        """It add a new meaning via its fields."""
        self._meanings.append(meaning.Meaning.create_meaning(pos,
                                                             case,
                                                             class_,
                                                             definition,
                                                             level))

    def add_meaning(self, nu_meaning: meaning.Meaning):
        """It adds a new meaning."""
        if isinstance(nu_meaning, meaning.Meaning):
            self._meanings.append(nu_meaning)

    def add_meaning_list(self, nu_meanings: list):
        """It adds multiple meanings from a list."""
        self._meanings = self._meaning_loop(nu_meanings)

    def add_origin(self, nu_origin: str):
        """Add or modify origin."""
        self._origin = nu_origin.lstrip(self.ORIGIN_CHAR).strip()

    def add_comment(self, nu_comment: str):
        """Add or modify comment."""
        self._comment = nu_comment.lstrip(self.COMMENT_CHAR).strip()

    def add_see(self, nu_see: str):
        """Add or modify see."""
        self._see = nu_see.lstrip(self.SEE_CHAR)

    def id(self):
        """Get id."""
        return self._id

    def word(self):
        """Get word."""
        return self._word

    def description(self):
        """Get description."""
        return self._description

    def pronunciation(self):
        """Get pronunciation."""
        return self._pronunciation

    def meanings(self) -> list:
        """Get meanings as a list."""
        return self._meanings or [""]

    def get_meanings_as_string(self) -> str:
        """Get meanings as a formatted string."""
        return "\n".join(str(m) for m in self._meanings)

    def get_meanings_as_list(self) -> list:
        """
        It returns the meanings as a list.

        See:
            Meaning.get_meaning()
        """
        return [m for m in self.meanings()]

    def origin(self):
        """Get origin."""
        return self._origin

    def comment(self):
        """Get comment."""
        return self._comment

    def see(self):
        """Get see."""
        return self._see

    def __add__(self, meaning_: meaning.Meaning):
        """
        It adds a new meaning.

        It's only a little syntactic sugar, and if we don't want to save
        into a new Entry instance it is equal to 'e += m' (see: Examples).

        Examples:
            # e: Entry, m: Meaning[, e2: Entry]
            e += m
            e = e + m
            e2 = e + m

        Return:
            The current Entry instance with the a new Meaning instance.
        """
        self.add_meaning(meaning_)
        return self

    def __str__(self):
        """Return a wannabe well-formated string."""
        return ("id: {id}, word: {word} /{pro}/\n"
                "description: {desc}\n"
                "{means}\n"
                "origin: {orig}\n"
                "comment: {comm}\n"
                "see: {see}\n").format(id=self.id(),
                                       word=self.word(),
                                       pro=self.pronunciation(),
                                       desc=self.description(),
                                       means=self.get_meanings_as_string(),
                                       orig=self.origin(),
                                       comm=self.comment(),
                                       see=self.see())

    def add_entry_part(self, text: str, indentchar: str):
        """It is the main method to add a new part to an entry or a meaning."""
        if len(indentchar) != 1:
            indentchar = indentchar[0]

        tmpm = meaning.Meaning.is_meaning(text, indentchar)
        if tmpm:
            self += meaning.Meaning(*tmpm)
        else:
            prefix = text[0]
            if prefix == self.PRONOUNCIATION_CHAR:
                self.add_pronunciation(text)
            elif prefix == self.ORIGIN_CHAR:
                self.add_origin(text)
            elif prefix == self.COMMENT_CHAR:
                self.add_comment(text)
            elif prefix == self.SEE_CHAR:
                self.add_see(text)
            else:
                self.add_description(text)

    def get_entry_as_dict(self) -> dict:
        """
        It returns a whole entry (with its meanings) as a dictionary.

        Keys:
            idx -- the id
            wrd -- the word itself (that is all for)
            pro -- pronunciation
            dsc -- description (NOT meaning)
            mea -- meanings as array. Every meaning has these keys:
                   pos, cas, cls, def, lvl (for more, see
                   Meaning.get_meanings()'s docstring.
            ori -- Hallowed are the Ori! (it's the origin btw)
            com -- comment (unnecessary details, fun facts, whatever you want)
            see -- see also
        """
        return {'idx': self.id(),
                'wrd': self.word(),
                'pro': self.pronunciation(),
                'dsc': self.description(),
                'mea': self.get_meanings_as_list(),
                'ori': self.origin(),
                'com': self.comment(),
                'see': self.see()}
