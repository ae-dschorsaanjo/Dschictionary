# Dschictionary
It's a simple dictionary program mainly for hobby-linguists like me.

The main idea for this was that I needed an easy-to-use dictionary program with an easy input method/type.
Then I didn't find any program that'd be good for me, so I decided to make my own.

Input format
============

File format
-----------

File's have only an initial line to define languages in the following form:
language of words -> language of definitions

It is the default form, you can change the separator (->) within the dschictionary_class.py.

In the rest of the file is the entries themself, separated by a blank line.

Entry format
------------

An entry can have these parts:
* word
* pronunciation
* description (short description about the word)
* origin
* comment (any additional information about the word)
* see also (related words)
* meanings

One entry can have more then one meaning definition, for more see the Meaning format.
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
The *part of speech* is in a prefix form, you can change these prefixes within the meaning.py file. By default it contains the needed part of speeches for znacra (a conlang of mine).
Indentation level is optional and has not a great effect yet.

__example__
(NOTE: pos = part of speech)

(pos+case:class) definition

---

For more examples, see try.dict (input file) and try.dict.txt (generated output).
