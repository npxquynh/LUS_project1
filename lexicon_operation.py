import re

def generate_lexicon_from_textfile(filename):
    with open(filename) as f:
        lexicon = set()
        for line in f:
            words = re.split('[ ]+', line.strip())
            for word in words:
                if not re.match('^\d.', word):
                    lexicon.add(word)

    return lexicon

def read_lexicon_file(filename):
    symbols = set()
    with open(filename) as f:
        for line in f:
            symbols.add(line.strip().split('\t')[0])

    # remove <epsilon> and <unk>
    try:
        symbols.remove('<epsilon>')
        symbols.remove('<unk>')
    except: # if no symbols found, it's still fine.
        pass
    return symbols

def write_lexicon_to_file(filename, lexicon):
    """
    set(): lexicon
    """
    # remove empty string character
    try:
        lexicon.remove('')
    except:
        pass

    count = 0

    special_lex = ['<epsilon>', '<unk>']
    lexicon = list(lexicon) # just in case lexicon is a set

    with open(filename, 'w') as output:
        for lex in special_lex + lexicon:
            output.write('%s\t%d\n' % (lex, count))
            count += 1