"""

"""


import dschictionary_class as dsch
import codecs


POS = dsch.entry.meaning.PART_OF_SPEECH


class BaseDschictionary():
    """
    Base class of a Dschictionary output.

    This contains every important functions that are needed for different
    output formats.

    This is also the output class of Dschictionary's input format (to sort the
    input file's entries).

    Function and method names that do not start with a single underscore are
    overridable" and/or public.
    """

    _dschict = None  # Dschictionary instance
    _fname = ''  # filename
    _pos = {}  # used PoSs

    def __init__(self, filename):
        """
        It reads and processes a file.

        Parameters:
            filename -- name of the dschictionary file
        """
        if filename:
            self._fname = filename
            self._dschict = dsch.Dschictionary.create_dschictionary(filename)
        else:
            self.error("Filename is not given or not valid!")

    def dschictionary(self):
        """Returns the used dschictionary instance."""
        return self._dschict

    def status(self, message, category=''):
        """
        It writes the status messages.

        Parameters:
            message -- The status message (string)
        """
        if category:
            message = "{cat:5} -- {msg}".format(
                          cat=str(category)[:5].upper(),
                          msg=message)
        print(message)

    def error(self, message):
        """
        It writes the error messages.

        Parameters:
            message -- The error message (string)
        """
        print("ERROR --", message)

    def _add_pos(self, pos):
        """
        Adds a pos to the pos list.

        Parameters:
            pos -- PoS to be added
        """
        if pos in POS:
            self._pos[pos] = POS[pos]
        else:
            self._pos[pos] = 'Unknown part of speech'

    def _get_filename(self, filename):
        return filename or self._fname.split('.')[0]

    def _filename(self, filename, ex='txt', add='dict'):
        """
        Returns the output filename.

        Parameters:
            filename -- Filename (string)
            ext -- Output file's format (string, default: 'txt')
            add -- Additional pre-extension (string, default: 'dict')

        Returns:
            Filename of output file (filename.add.ext)
        """
        filename = filename.split('.')[0]

        filename += ('.' + add if add else '') + ('.' + ex if ex else '')
        return filename

    def _filewrite(self, filename, out):
        """
        It is a simple file writer function (for utf-8 encoded files).

        Parameters:
            filename -- Output file's name (with extension) (string)
            out -- Processed data (string)
        """
        codecs.open(filename, 'w', 'utf-8').write(out)


    def _fileswap(self, filename, backupfilename, out):
        """
        It is a file swapper function that makes a backup of the original
        input file and then generates a new one (input format and sorted).

        Parameters:
            filename -- Input file's name (with extension) (string)
            backupfilename -- Backup file's name (with extension) (string)
            out -- Processed data (string)
        """
        f = open(filename, 'r')
        codecs.open(backupfilename, 'w', 'utf-8').write(f.read())
        codecs.open(filename, 'w', 'utf-8').write(out)


    def _initialize(self, filename, ex='txt'):
        """
        Initializes the needed variables for outputs.

        Parameters:
            filename -- Filename (string)
            ex -- Extension of the file (string, default: 'txt')

        Return:
            (dschictionary instance, filename, title, entry_lang and def_lang)
        """
        d = self._dschict
        return (d, self._filename(filename, ex),
                d.title(), d.entry_language, d.definition_language)

    def _write_dschict_info(self, title, el, dl,
                            langsep=dsch.LANGUAGE_SEPARATOR,
                            _format=("{fromlang} {langsep} {tolang}\n")):
        """
        Returns a formatted string of the elementary dschictionary information.
        The format input can contain the following flags:
            {title} -- title,
            {fromlang} -- entry language (el),
            {langsep} -- language separator (langsep),
            {tolang} -- definition language (dl)

        Parameters:
            title -- Title of dschictionary
            el -- Entries' language
            dl -- Definitions' language
            langsep -- Language separator
            _format -- Format string for output

        Return:
            Formatted string
        """
        return _format.format(title=title,
                              fromlang=el,
                              langsep=langsep,
                              tolang=dl)

    def _write_entry_header(self, word, pro, desc,
                            proc=dsch.entry.Entry.PRONOUNCIATION_CHAR,
                            id_prefix='dsch', line='-',
                            _format="\n{word} /{pro}/\n{desc}\n"):
        """
        Returns a formatted string of an entry's header.
        The formatted input can contain the following flags:
            {id} -- entry id (id_prefix-word, for HTML),
            {word} -- word,
            {pro} -- pronunciation,
            {proc} -- pronunciation char,
            {desc} -- description,
            {line} -- word-header separator line (for txt)

        Parameters:
            word -- Word
            pro -- Pronunciation
            desc -- Description
            proc -- Pronunciation char (borders)
            id_prefix -- Id prefix
            line -- Line
            _format -- Format string for output

        Return:
            Formatted string
        """
        return _format.format(id=id_prefix+'-'+word,
                              word=word,
                              pro=pro,
                              proc=proc,
                              desc=desc,
                              line='-'*len(word))

    def _write_meaning(self, ind, pos, class_, case, def_,
                       pid='dsch-pos', clsc=':', casc='+', indc=' ',
                       _format=("{indc}({pos}{clsc}{cls}{casc}{cas})"
                                " {def_}\n")):
        """
        Returns a formatted string of a meaning.
        The formatted input can contain the following flags:
            {ind} -- indentation length,
            {indc} -- indentation,
            {pid} -- part of speech's id,
            {pos} -- part of speech,
            {cls} -- class,
            {cas} -- case,
            {clsc} -- class character,
            {casc} -- case character,
            {def_} -- meaning definition

        Parameters:
            ind -- Indentation level (int),
            pos -- Part of speech (string),
            class_ -- Class (string),
            case -- Case (string),
            def_ -- Definition (string),
            pid -- PoS table id prefix (string, default: 'dsch-pos'),
            clsc -- Class character (string, default: ':'),
            casc -- Case character (string, default: '+'),
            indc -- Indentation character (string, default: ' '),
            _format -- Format string for output

        Return:
            Formatted string
        """
        try:
            ind = int(ind)
        except:
            ind = 0
        return _format.format(ind=int(ind),
                              indc=int(ind)*indc,
                              pid=pid+'-'+pos,
                              pos=pos,
                              clsc=clsc if class_ else '',
                              cls=class_,
                              casc=casc if case else '',
                              cas=case,
                              def_=def_)

    def _write_entry_footer(self, orig, comm, see,
                            orig_prefix=dsch.entry.Entry.ORIGIN_CHAR,
                            comm_prefix=dsch.entry.Entry.COMMENT_CHAR,
                            see_prefix=dsch.entry.Entry.SEE_CHAR,
                            _format=("{op}{orig}"
                                     "{cp}{comm}"
                                     "{sp}{see}"),
                            see_format_=''):
        """
        Returns a formatted string of an entry's footer.
        The formatted input can contain the following flags:
            {op} -- word's origin prefix character
            {orig} -- word's origin
            {cp} -- comment's prefix character
            {comm} -- comment about the word
            {sp} -- see also's prefix character
            {see} -- see also words
        The _see_format can contain the following flags:
            {id} -- the 'see also' word's id
            {w} -- the 'see also' word

        Parameters:
            orig -- Word's origin,
            comm -- Comment about the word,
            see -- See also these words,
            orig_prefix -- Word's origin prefix character,
            comm_prefix -- Comment's prefix character,
            see_prefix -- See also's prefix character,
            _format -- Format string for output,
            _see_format -- See also word's format string

        Return:
            Formatted string
        """
        if not see_format_:
            see_format_ = "{w}"
        tmp = see.split(',')
        see = ''
        for t in tmp:
            see += see_format_.format(id='dsch-'+t.strip(),
                                        w=t.strip())

        return _format.format(op=(orig_prefix + ' ') if orig else '',
                              orig=orig + ('\n' if orig else ''),
                              cp=(comm_prefix + ' ') if comm else '',
                              comm=comm + ('\n' if comm else ''),
                              sp=(see_prefix + ' ') if see else '',
                              see=see + ('\n' if see else ''))

    def _write_POS_cycle(self, before, after, prefix, _format):
        """
        This is the inner cycle of the self._write_POS function.
        This also adds the 'before' and 'after' to the output.
        Parameters are the same.
        """
        keys = self._pos
        out = before
        for k in sorted(keys):
            out += _format.format(k=k, v=keys[k], id=prefix+'-'+k)
        return out + after

    def _write_POS(self, before='', after='',
                   eid_prefix='dsch-pos', _format=''):
        """
        Return a formatted string of a table of used Part of Speeches.
        The _format string is for a single entry!
        The formatted input can contain the following flags:
            {k} -- key of a PoS (from self._pos)
            {v} -- name of a PoS (from POS constant)
            {id} -- id of an entry

        Parameters:
            before -- This text will be before the formatted entries.
            after -- This text will be after the formatted entries.
            eid_prefix -- Id prefix of an entry (for HTML)
            _format -- Formatted string of an entry

        Return:
            Formatted string
        """
        return self._write_POS_cycle(before, after, eid_prefix,
                                     _format) if _format else ''  # there is no
                                                                  # POS table
                                                                  # in input
                                                                  # files

    def _write_sign(self, _format=""):
        """
        Returns a formatted string of the sign.
        The formatted input can contain the following flags:
            {pre} -- text before the program's name,
            {link} -- link to the source,
            {name} -- the program's name

        Parameters:
            _format -- Format string of the sign

        Return:
            Formatted string
        """
        return _format.format(pre="Created via",
                              link=("https://github.com/ae-dschorsaanjo/"
                                    "Dschictionary"),
                              name='Dschictionary')

    def write_dschictionary(self, ex='txt', filename=None):
        """
        TODO: docstring

        Parameters:
            ex -- Output file's extension
            filename -- This is the output file's filename. If None, then
                        the filename will be used that was used to read the
                        input.

        Return:
            Formatted string
        """
        # Initialize the writing
        self.status('Start writing.', 'start')
        d, filename, ttl, el, dl = self._initialize(
                                                self._get_filename(filename),
                                                ex)
        idx = 0
        self.status('Initializing is done.', 'init')

        # Add dschictionary info
        out += self._write_dschict_info(ttl, el, dl)
        self.status('Basic informations', 'write')

        # Add entries
        for e in d.entries():
            idx += 1
            ed = e.get_entry_as_dict()

            # Add entry header
            out += self._write_entry_header(ed['wrd'], ed['pro'], ed['dsc'])

            # Add meanings
            for m in ed['mea']:
                if not m:
                    break
                md = m.get_meaning_as_dict()

                pos = md['pos']
                if pos not in self._pos:
                    self._add_pos(pos)

                out += self._write_meaning(md['lvl'], pos, md['cls'], md['cas'],
                                           md['def'])

            # Add entry footer
            out += self._write_entry_footer(ed['ori'], ed['com'], ed['see'])
            self.status('Entry #' + str(idx), 'write')
        self.status('Entries done', 'write')

        # Add Part of Speeches' table
        out += self._write_POS()
        self.status('PoS table', 'write')

        # Add sign
        out += self._write_sign()
        self.status('Sign', 'write')

        # Write (usually it's by the self._filewrite function)
        self._fileswap(self._fname, self._filename('', ex, 'backup'),
                       out)
        self.status('File writing is done', 'file')
        self.status('Everything is done!', 'end')


class TextDschictionary(BaseDschictionary):
    """
    Dschictionary output class for plain text output.
    """

    def __init__(self, filename):
        """Only a filename all you need."""
        super().__init__(filename)

    def write_dschictionary(self, ex='txt', filename=None):
        """Return a simple txt file"""
        d, filename, ttl, el, dl = self._initialize(
                                                self._get_filename(filename),
                                                ex)
        idx = 0

        out = self._write_dschict_info(ttl, el, dl,
                                       _format=("{title} "
                                                "({fromlang} - {tolang})\n\n"))

        entry_head_format = '{word}  {proc}{pro}{proc}\n{line}\n"{desc}"\n'
        meaning_format = "{indc}({pos}{clsc}{cls}{casc}{cas}) {def_}\n"
        entry_foot_format = "{op}{orig}{cp}{comm}{sp}{see}\n\n"
        pos_table_format = ""

        for e in d.entries():
            ed = e.get_entry_as_dict()
            out += self._write_entry_header(ed['wrd'], ed['pro'], ed['dsc'],
                                            line='-'*len(ed['wrd']),
                                            _format=entry_head_format)

            for m in ed['mea']:
                if not m:
                    break
                md = m.get_meaning_as_dict()

                pos = md['pos']
                if pos not in self._pos:
                    self._add_pos(pos)

                out += self._write_meaning(md['lvl'], md['pos'], md['cls'],
                                           md['cas'], md['def'],
                                           _format=meaning_format)

            out += self._write_entry_footer(ed['ori'], ed['com'], ed['see'],
                                            'origin: ', 'comment: ',
                                            'see also: ',
                                            _format=entry_foot_format)

        line = '-' * 40 + "\n"
        out += self._write_POS(line, line, _format="{k:>4}: {v}\n")
        out += self._write_sign("\n{pre} {name}\n\n")
        self._filewrite(self._filename(filename, ex), out)

class HTMLDschictionary(BaseDschictionary):
    """
    Dschictionary output class for HTML output.
    """

    def __init__(self, filename):
        """Only a filename all you need."""
        super().__init__(filename)

    def _add_style(self):
        """Returns the CSS styles to the output HTML file."""
        with open('dschict.css', 'r') as f:
            style = f.read()
        return "<style>\n" + style + "</style>"

    def write_dschictionary(self, ex='html', filename=None):
        """Writer function."""
        d, filename, ttl, el, dl = self._initialize(
                                                self._get_filename(filename),
                                                ex)
        idx = 0

        out = self._add_style()

        out += "<article class='dsch'>"

        out += self._write_dschict_info(ttl, el, dl, _format=("<h1>{title}</h1>"
                                                              "<h3>{fromlang}"
                                                              "&nbsp;-&nbsp;"
                                                              "{tolang}</h3>"))

        entry_head_format = ("\n<a class='word' id='{id}' href='#{id}'>"
                             "{word}</a>&nbsp;<span class='pro'>{proc}{pro}"
                             "{proc}</span><br>\n<i class='desc'>{desc}</i>\n")

        meaning_format = ("<tr class='mean' style='padding-left: {ind}ch;'>"
                          "<td class='type'>(<span class='pos'><a href='#{pid}"
                          "'>{pos}</a></span><span class='cls'>{clsc}{cls}"
                          "</span><span class='cas'>{casc}{cas}</span>)</td>"
                          "<td>{def_}</td></tr>\n")

        entry_foot_format = ("<span class='orig'>{op}{orig}</span>"
                             "<span class='comm'>{cp}{comm}</span>"
                             "<span class='see'>{sp}{see}</span>")
        entry_see_format = "<a href='#{id}'>{w}</a> "
        pos_table_format = ("<tr><td id='{id}' style='text-align: right; "
                            "padding-right: 1ch;'>{k}</td><td style='"
                            "padding-left: 1ch;'>{v}</td></tr>\n")
        for e in d.entries():
            idx += 1
            ed = e.get_entry_as_dict()
            out += "<div class='entry'>\n"
            out += self._write_entry_header(ed['wrd'], ed['pro'], ed['dsc'],
                                            _format=entry_head_format)

            out += "<table class='meaning'>"
            for m in ed['mea']:
                if not m:
                    break
                md = m.get_meaning_as_dict()

                pos = md['pos']
                if pos not in self._pos:
                    self._add_pos(pos)

                out += self._write_meaning(md['lvl'], md['pos'], md['cls'],
                                           md['cas'], md['def'],
                                           _format=meaning_format)
            out += "</table>\n<div class='add'>"

            out += self._write_entry_footer(ed['ori'], ed['com'], ed['see'],
                                            'origin: ', 'comment: ',
                                            'see also: ',
                                            _format=entry_foot_format,
                                            see_format_=entry_see_format)

            out += "</div></div>"

        out += self._write_POS(("<table class='postab' style='border: "
                                "1px solid black;'>\n"), "</table>\n",
                                _format=pos_table_format)

        out += self._write_sign("<div class='via'><hr><span class='via'>"
                                "{pre} <a href='{link}'>{name}</a>"
                                "</span></div>\n")

        out += "</articles>"

        self._filewrite(self._filename(filename, ex), out)


# 4 tests only
if __name__ == '__main__':
    fn = 'example.txt'
    # test = BaseDschictionary(fn)
    # test.write_dschictionary('txt')
    print('reorder is done')
    test = TextDschictionary(fn)
    test.write_dschictionary()
    print('txt write is done')
    test = HTMLDschictionary(fn)
    test.write_dschictionary()
    print('html write is done')
