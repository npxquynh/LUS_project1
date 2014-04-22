import pdb
LEX_FILE = './lex/lexicon.txt'

def gen_weekdays():
    weekdays = [
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday'
    ]

    abbr_weekdays = [x[0:3] for x in weekdays]
    abbr_weekdays.append('thur')

    plural_weekdays = ['%ss' % x for x in weekdays]

    return weekdays + abbr_weekdays + plural_weekdays

def gen_months():
    months = [
        'january',
        'february',
        'march',
        'april',
        'may',
        'june',
        'july',
        'august',
        'september',
        'october',
        'november',
        'december'
    ]

    abbr_months = [x[0:3] for x in months]

    return months + abbr_months

def gen_ordinal_numbers():
    ordinal_numbers = []

    base_ordinal_numbers = [
        'first',
        'second',
        'third',
        'fourth',
        'fifth',
        'sixth',
        'seventh',
        'eighth',
        'ninth',
    ]
    [ordinal_numbers.append(x) for x in base_ordinal_numbers]

    special_ordinal_numbers = [
        'tenth',
        'eleventh',
        'twelfth',
        'thirteenth',
        'fourteenth',
        'fifteenth',
        'sixteenth',
        'seventeenth'
        'eighthteenth',
        'nineteenth',
        'twentyth',
    ]
    [ordinal_numbers.append(x) for x in special_ordinal_numbers]

    prefix = ['twenty', 'thirty']
    ordinal_numbers.append('twentieth')
    ordinal_numbers.append('thirtieth')
    for p in prefix:
        for x in base_ordinal_numbers:
            ordinal_numbers.append('%s-%s' % (p, x))

    return ordinal_numbers


def gen_numbers():
    numbers = []
    base_numbers = 'one two three four five six seven eight nine'.split(' ')
    [numbers.append(x) for x in base_numbers]

    special_numbers = 'ten eleven twelve thirteen fourthteen fifteen sixteen seventeen eighthteen nineteen'.split(' ')
    [numbers.append(x) for x in special_numbers]


    prefix = ['twenty', 'thirty']
    [numbers.append(x) for x in prefix]
    for p in prefix:
        for x in base_numbers:
            numbers.append('%s-%s' % (p, x))

    return numbers

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
    lexicon = read_base_lex('./lex/base_lexicon.txt')
    lexicon += gen_weekdays()
    lexicon += gen_months()
    lexicon += gen_ordinal_numbers()
    lexicon += gen_numbers()

    write_lexicon_to_file(LEX_FILE, lexicon)

