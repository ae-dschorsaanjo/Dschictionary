# Dschictionary
It's a simple dictionary program mainly for hobby-linguists like me, or for anyone else who find it interesting or useful.

It's input's format is simple as the 1*1, the prefixes are mostly unambiguous and the input file is a simple (UTF-8 encoded) plain text file.

The idea for this was that I needed an easy-to-use dictionary program with an easy input method/type.
Then I didn't find any program that'd be good for me, so I decided to make my own.

Input format
============

File format
-----------

File's have only an initial line to define languages in the following way:
*language of words -> language of definitions*

It is the default form, you can change the separator (->) within the dschictionary_class.py.

In the rest of the file is the entries themself, separated by a blank line.

Entry format
------------

An entry can have these parts:
* word
* pronunciation
* description (about the word)
* origin
* comment (any additional information)
* see also (related words)
* meanings

One entry can have more than one meaning definition, for more see the Meaning format.
*Only the word* is required, any other part is optional!
Pronunciation can be next to the word or in a line beneath the word.

Meaning format
--------------

A meaning can have these parts:
* part of speech (noun, verb, etc in prefix form)
* case (word's case)
* class (word's class)
* definition (it is the actual meaning)
* level (level of indentation)

The *case* and *class* parts can be almost anything, it depends on the language.
The *part of speech* is in a prefix form, you can change these prefixes within the meaning.py file. By default it contains the needed part of speeches for znacra and toki pona.
Indentation level is optional and has not a great or any effect yet.

__example__
(NOTE: pos = part of speech)

(pos:class+case) definition

---

For more examples, see example.txt (input file) and example.dict.* (generated output).
