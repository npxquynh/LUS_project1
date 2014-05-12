import csv
import pdb

import common_functions as cf
import lexicon_operation as lex

LEX_FILE = './lex/lex_ngramsymbols.syms'
W2CLASS_MANUALLY_ANNOTATED_FILENAME = './w2class/w2class_manually_annotated.txt'

class W2Class():
    W2CLASS_TRANSDUCER_FILENAME = './w2class/w2class.fsm'

    def __init__(self, symbols):
        self.lexicon = symbols # set(): all lexicon
        # will be updated constantly, to contain only symbol that is not mapped to
        # associated class
        self.symbols = symbols
        self.freq_words = set()
        self.class_name = set()

    # dayname
    @staticmethod
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

    @staticmethod
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

    @staticmethod
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
            'seventeenth',
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

    @staticmethod
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

    @staticmethod
    def gen_airport_cityname(filename):
        """
        http://openflights.org/data.html
        """
        cities = set()
        airports = set()
        airport_codes = set()

        with open(filename) as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    # if row[3] == 'United States':
                    cities.add(row[2])
                    airports.add(row[1])
                    airport_codes.add(row[4])
                except:
                    pass

        cities = cf.process_text(cities)
        airports = cf.process_text(airports)
        airport_codes = cf.process_text(airport_codes)

        return cities, airports, airport_codes

    @staticmethod
    def gen_state_name(filename):
        """
        http://www.50states.com/tools/postal.htm
        """
        state_names = set()
        state_codes = set()

        with open(filename) as f:
            for line in f:
                words = line.strip().split('\t')
                try:
                    state_names.add(words[0])
                    state_codes.add(words[1])
                except:
                    pass
        state_names = cf.process_text(state_names)
        state_codes = cf.process_text(state_codes)

        return state_names, state_codes

    def gen_frequent_words(self, filename):
        """
        http://www.rupert.id.au/resources/1-1000.txt

        there are some words that can cause confusion, e.g. "in" can be (i)
        abbreviation for state Indiana or (ii) the preposition. So I'll try to
        add more arch to transducer
        """
        word_list = set()
        count = 0
        with open(filename) as f:
            for line in f:
                if (len(line) <= 7):
                    word_list.add(line.strip())

        self.freq_words = word_list
        return word_list

    def gen_w2class_manually_annotated(self, filename):
        with open(filename) as f:
            reader = csv.reader(f, quoting=csv.QUOTE_NONE)
            for row in reader:
                class_name = row[0]
                word_list = row[1].strip().split(' ')
                self.write_w2class_transducer(word_list, class_name)

    def manage_lexicon(self, word_list, class_name):
        """
        remove those words in wordlist from 'symbols'
        update new words that are not presented in lexicon
        """
        word_list = set(word_list)
        self.lexicon = self.lexicon.union(word_list)
        self.class_name.add(class_name)
        self.symbols = self.symbols.difference(word_list)

    def write_w2class_transducer(self, word_list, class_name):
        self.manage_lexicon(word_list, class_name)

        filename = self.W2CLASS_TRANSDUCER_FILENAME
        with open(filename, 'a') as output:
            if len(class_name) != 0:
                for word in word_list:
                    output.write('%d\t%d\t%s\t%s\n' % (0, 0, word, class_name))
            else:
                for word in word_list:
                    output.write('%d\t%d\t%s\t%s\n' % (0, 0, word, word))

    def write_word_without_associated_class(self, filename):
        word_list = set()
        word_list = word_list.union(self.freq_words)
        word_list = word_list.union(self.symbols)

        with open(filename, 'w') as output:
            output.write('\n'.join(word_list))

    def update_lexicon(self, filename):
        lexicon = self.lexicon.union(self.class_name)
        lex.write_lexicon_to_file(filename, list(lexicon))

        self.write_w2class_transducer(self.symbols, '')

    def write_last_line_w2class_transducer(self):
        with open(self.W2CLASS_TRANSDUCER_FILENAME, 'a') as output:
            # special case <unk>:<unk>
            output.write('%d\t%d\t%s\t%s\n' % (0, 0, '<unk>', '<unk>'))
            output.write('0\n')

def gen_concept_classes(concept_filename):
    concept_classes = set()
    with open(concept_filename) as f:
        for line in f:
            concept_classes.add(line.strip().split('.')[-1])

    with open('./tmp/concept_classes.txt', 'w') as output:
        for concept in concept_classes:
            output.write('%s\n' % concept)


if __name__ == '__main__':
    symbols = lex.read_lexicon_file(LEX_FILE)

    w2class = W2Class(symbols)

    tmp = w2class.gen_weekdays()
    w2class.write_w2class_transducer(tmp, 'day_name')

    tmp = w2class.gen_months()
    w2class.write_w2class_transducer(tmp, 'month_name')

    tmp = w2class.gen_ordinal_numbers()
    w2class.write_w2class_transducer(tmp, 'day_number')

    tmp = w2class.gen_numbers()
    w2class.write_w2class_transducer(tmp, 'day_number')

    tmp1, tmp2, tmp3 = w2class.gen_airport_cityname('./w2class/airports.dat')
    w2class.write_w2class_transducer(tmp1, 'city_name')
    w2class.write_w2class_transducer(tmp2, 'airport_name')
    w2class.write_w2class_transducer(tmp3, 'airport_code')

    tmp1, tmp2 = w2class.gen_state_name('./w2class/state.txt')
    w2class.write_w2class_transducer(tmp1, 'state_name')
    w2class.write_w2class_transducer(tmp2, 'state_code')

    tmp = w2class.gen_frequent_words('./w2class/1-1000.txt')
    w2class.write_w2class_transducer(tmp, '')

    w2class.gen_w2class_manually_annotated(W2CLASS_MANUALLY_ANNOTATED_FILENAME)

    # DO NOT DELETE THE FOLLOWING LINE
    w2class.write_word_without_associated_class('./w2class/word_without_class.txt')
    w2class.write_last_line_w2class_transducer()
    w2class.update_lexicon(LEX_FILE)



