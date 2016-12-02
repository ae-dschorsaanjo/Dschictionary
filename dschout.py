"""
This module contains every dschictionary-child for different outputs.

Please write your own output-classes here!
"""


__copyright__ = "Copyright (C) 2016, B. Zolt'n Gorza"


import dschictionary_class as dsch
from meaning import PART_OF_SPEECH


class TextDschictionary():
    """Basic pure text output."""

    _dschict = None  # Dschictionary instance
    _fname = ""  # future filename

    def __init__(self, filename):
        """
        It reads and processes a file.

        Parameters:
            filename -- name of the dschictionary file
        """
        if filename:
            self._dschict = dsch.Dschictionary.create_dschictionary(filename)
            self._fname = filename
        else:
            print("ERROR -- Filename isn't given or not valid!")

    def dschictionary(self):
        return self._dschict

    def _write_POS(self):
        keys = PART_OF_SPEECH.keys()
        line = "-" * 40
        out = "\n\n" + line + "\n"
        for k in sorted(keys):
            out += "{k:4s}: {v}\n".format(k=k,
                                          v=PART_OF_SPEECH[k])
        return out + line + "\n\n"

    def write_dschictionary(self,
                            filename="",
                            indentchar=dsch.DEFAULT_INDENT_CHAR,
                            indentnum=1):
        """It is writing a dschictionary into a file."""
        d = self._dschict
        if not filename:
            tmp = self._fname.split(".")
            filename = ".".join([tmp[i] for i in range(len(tmp)-1)])
            filename += ".dict.txt"

        # Add dschictionary info
        ttl = d.title()
        el = d.entry_language
        dl = d.definition_language
        out = ("{title} ({fromlang} - {tolang})\n"
               " \n").format(title=ttl,
                             fromlang=el,
                             tolang=dl)

        # Add entries
        for e in d.entries():
            ed = e.get_entry_as_dict()  # entry dictionary
            pro = (" /" + ed['pro'] + "/") if ed['pro'] else ""
            line = "-" * (len(ed['wrd'] + pro))
            desc = ('"' + ed['dsc'] + '"\n') if ed['dsc'] else ""

            out += ("\n{word}{pro}\n"
                    "{line}\n"
                    "{desc}").format(word=ed['wrd'],
                                     pro=pro,
                                     line=line,
                                     desc=desc)
            # Add meanings from an entry
            for m in ed['mea']:
                if not m:
                    break
                md = m.get_meaning_as_dict()  # meaning dictionary
                indent = indentchar * (indentnum * md['lvl'])
                case = " + " + md['cas'] if md['cas'] else ""
                class_ = " : " + md['cls'] if md['cls'] else ""

                out += ("{indent}"
                        "({pos}{cls}{cas}) "
                        "{def_}\n").format(indent=indent,
                                           pos=md['pos'],
                                           cas=case,
                                           cls=class_,
                                           def_=md['def'])
            # Rest of the entry's data
            orig = ("origin: " + ed['ori'] + '\n') if ed['ori'] else ""
            comm = ("/* " + ed['com'] + " */" + '\n') if ed['com'] else ""
            see = ("see also: " + ed['see'] + '\n') if ed['see'] else ""

            out += ("{orig}{comm}"
                    "{see}\n").format(orig=orig,
                                      comm=comm,
                                      see=see)
        # --- Additional things
        out += self._write_POS()
        out += " \n \nCreated via Dschictionary.py\n"
        f = open(filename, "w")
        f.write(out)
        f.close()

if __name__ == '__main__':
    test = TextDschictionary("try.dict")
    test.write_dschictionary()
    print("writing is done")

# TODO:
#     dokumentacio MINDENHEZ (min dict formatum,
#                                 hasznalat,
#                                 es pydoc legyen eleg a kodrol)
