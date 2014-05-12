import pdb
import lexicon_operation as lex

TRAINING_FILE = './data/atis.hlti.train'
LEX_FILE = './lex/lex_ngramsymbols.original'

def read_base_lex(filename):
    lexicon = []
    with open(filename) as f:
        for line in f:
            lexicon.append(line.strip())

    return lexicon

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

if __name__ == '__main__':
    lexicon = lex.generate_lexicon_from_textfile(TRAINING_FILE)
    lex.write_lexicon_to_file(LEX_FILE, lexicon)
