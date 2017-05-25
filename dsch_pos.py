"""Part of Speeches' definitions -- It's a kind of config file."""

# Default definitions and shortenings
# These definitions should be enough for in most cases (especially for conlangs)
ENGLISH = {
    # General PoSs
    'n':   'noun',
    'pn':  'pronoun',
    'pv':  'pre-verb',
    'v':   'verb',
    'vt':  'transitive verb',
    'vi':  'intransitive verb',
    'pre': 'preposition',
    'c':   'conjunction',
    'i':   'interjection',
    'art': 'article',
    'adj': 'adjective',
    'adv': 'adverb',

    # Not usual, but yet possible PoSs (for natural languages)
    'p':   'particle, invariant word or grammatical word',
    'fun': 'function word',

    # For conlangs
    'ad':  'adjective or adverb',
    's':   'specifier',
    'm':   'modifier',
    'ma':  'marker',
    'sp':  'special particle',
    'stm': 'sentence type marker',
    # Others to make relations to other languages
    'tp':  '(closest) toki pona equivalent',
    'eng': 'related English word(s)',
    'hun': 'related Hungarian word(s)',
    'esp': 'related Esperanto word(s)'
}

# This is/was experimental, maybe will have some use in the future.
HUNGARIAN = {
    'n':   'főnév',
    'pv':  'segédige',
    'v':   'ige',
    's':   'specifier',
    'p':   'egyéb',
    'm':   'jelölő',
    'sp':  'speciális egyéb',
    'stm': 'mondattípus határozó',
    'tp':  'toki pona',  # 'closest toki pona equivalent'
    # others that are not for znacra (in other words, they're for toki pona)
    'adj': 'melléknév',
    'adv': 'határozószó',
    'pre': 'előljáró'
}

DEFAULT = ENGLISH

ALL_POS = {
    'eng': ENGLISH,
    'hun': HUNGARIAN
}
