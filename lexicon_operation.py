

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

    with open(filename, 'w') as output:
        for lex in special_lex + lexicon:
            output.write('%s\t%d\n' % (lex, count))
            count += 1