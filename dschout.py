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
        """
        Returns the dschictionary to be formatted.
        """
        return self._dschict

    def _filename(self, filename, ext="txt"):
        """
        Returns the output filename.

        Parameters:
            filename -- output name
            ext -- output file's format

        Returns:
            Filename for output
        """
        if not filename:
            tmp = self._fname.split(".")
            filename = ".".join([tmp[i] for i in range(len(tmp)-1)])

        filename += ".dict" + ("." + ext if ext else "")
        return filename

    def _initialize(self, filename, ex="txt"):
        """Initialize the needed variables for output."""
        d = self._dschict
        return (d, self._filename(filename, ex), 
                d.title(), d.entry_language, d.definition_language)

    def _write_dschict_info(self, title, el, dl,
                            _format="{title} ({fromlang} - {tolang})\n"):
        """
        Returns a formatted string with the basic dschictionary information.
        The format input has to contain the followings: {title},
        {fromlang} (el), {tolang} (dl).

        Parameters:
            title -- Title of dschictionary
            el -- Entry's language
            dl -- Definition's language
            _format -- Format string for output (used with format() function)

        Return:
            Formatted string
        """
        return _format.format(title=title,
                              fromlang=el,
                              tolang=dl)

    def _write_POS(self):
        """
        Build the Part of speech table.
        """
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
        """
        It is writing a dschictionary into a file.
        
        Parameters:
            filename -- output filename
            indentchar -- character of indentation
            indentnum -- length of a level of indentation
        """
        d = self._dschict
        filename = self._filename(filename)

        # Add dschictionary info
        ttl = d.title()
        el = d.entry_language
        dl = d.definition_language
        out = self._write_dschict_info(d.title(), d.entry_language,
                                       d.definition_language)

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
        out += " \n \nCreated via Dschictionary\n"
        f = open(filename, "w")
        f.write(out)
        f.close()


class HTMLDschictionary(TextDschictionary):
    """
    TODO: dokumentary comm
    """

    def _write_POS(self):
        """
        FIXME: it's only a prototype
        """
        keys = PART_OF_SPEECH.keys()
        out = "<table class='postab' style='border: 1px solid black;'>\n"
        for k in sorted(keys):
            out += ("<tr><td style='text-align: right; padding-right: 1ch;'>"
                    "{k}</td><td style='padding-left: 1ch;'>"
                    "{v}</td></tr>\n").format(k=k, v=PART_OF_SPEECH[k])
        out += "</table>\n"
        return out

    def _add_style(self):
        f = open("dschict.css", 'r')
        style = f.read()
        f.close()
        return "<style>\n" + style + "</style>\n"

    def write_dschictionary(self,
                            filename="",
                            indentchar=dsch.DEFAULT_INDENT_CHAR,
                            indentnum=1,
                            inc_style=False):
        """
        It is writing a dschictionary into a HTML file.

        Parameters:
            filename -- output filename
            indentchar -- character of indentation
            indentnum -- length of a level of indentation
            inc_style -- include style (true) or link the css (false) UNUSED
        """
        d, filename, ttl, el, dl = self._initialize(filename, 'html')
        idx = 0
        
        out = self._add_style()

        out += "<article class='dsch'>"

        # Add dschictionary info
        out += self._write_dschict_info(ttl, el, dl,
                                       ("<h1>{title}</h1>"
                                        "<h3>{fromlang}&nbsp;"
                                        "-&nbsp;{tolang}</h3>\n"))
        
        # Add entries
        for e in d.entries():
            idx += 1
            ed = e.get_entry_as_dict()
            pro = ("<i>/" + ed['pro'] + "/</i>") if ed['pro'] else ""
            desc = ed['dsc'] or ""

            out += ("<div class='entry'>"
                    "<a class='word' id='{id}'>{word}</a>"
                    "&nbsp;<span class='pro'>{pro}</span><br>\n"
                    "<i class='desc'>{desc}</i>\n").format(
                        id=ed['wrd']+str(idx),
                        word=ed['wrd'],
                        pro=pro,
                        desc=desc)
            
            # Add meanings
            out += "<div class='meanings'>"
            for m in ed['mea']:
                if not m:
                    break
                md = m.get_meaning_as_dict()
                indent = indentnum * md['lvl']
                case = md['cas'] or ""
                class_ = md['cls'] or ""

                out += ("<span class='mean' style='margin-left: {ind}ch;'>"
                        "<i>(<span class='pos'>{pos}</span>"
                        "{clsc}<span class='cls'>{cls}</span>"
                        "{casc}<span class='cas'>{cas}</span>)</i>"
                        "&nbsp;{def_}"
                        "</span>\n").format(ind=indent,
                                          pos=md['pos'],
                                          cls=class_,
                                          clsc="+" if class_ else "",
                                          cas=case,
                                          casc=":" if case else "",
                                          def_=md['def'])
            out += "</div>\n"  # end of div.meanings

            # Rest of the entry's data
            out += "<div class='add'>"
            orig = ("<span class='orig'>origin: " 
                    + ed['ori'] + "</span>") if ed['ori'] else ""
            comm = ("<span class='comm'>comment: " 
                    + ed['com'] + "</span>") if ed['com'] else ""
            see = ("<span class='see'>see also: " 
                   + ed['see'] + "</span>") if ed['see'] else ""
                
            out += ("{comm}"
                    "{orig}"
                    "{see}").format(orig=orig,
                                    comm=comm,
                                    see=see)
            out += "</div>\n"  # end of additional data
            out += "</div>\n"  # end of entry

        out += self._write_POS()
        out += ("<div class='via'><hr><span class='via'>"
                "Created via Dschictionary"
                "</span></div>\n")
        out += "</articles>"
        f = open(filename, 'w')
        f.write(out)
        f.close()


if __name__ == '__main__':
    fn = "toki pona - toki Mosijo.txt"
    #test = TextDschictionary(fn)
    #test.write_dschictionary()
    #print("text writing is done")
    test2 = HTMLDschictionary(fn)
    test2.write_dschictionary()
    print("html writing is done")

# TODO:
#     dokumentacio MINDENHEZ (min dict formatum,
#                                 hasznalat,
#                                 es pydoc legyen eleg a kodrol)
