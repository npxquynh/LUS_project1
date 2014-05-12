import pdb
import common_functions as cf
import lexicon_operation as lex

LEX_FILE = './lex/lex_ngramsymbols.syms'
CONCEPT_FILENAME = './data/concepts'

class W2Concept():
    def __init__(self, concept_filename):
        self.concept_filename = concept_filename
        self.concepts = set()
        self.class_and_concept = dict()
        self.word_without_associated_class = set()

        self.class_to_concept()

    def set_word_without_associated_class(self, word_without_associated_class_filename):
        with open(word_without_associated_class_filename) as f:
            word_list = f.read().split('\n')
            self.word_without_associated_class = set(word_list)

    def class_to_concept(self):
        with open(self.concept_filename) as f:
            for line in f:
                concept = line.strip()
                self.concepts.add(concept)

                class_name = concept.split('.')[-1]

                if class_name not in self.class_and_concept:
                    self.class_and_concept[class_name] = set()

                self.class_and_concept[class_name].add(concept)

    def write_w2concept_transducer(self, filename):
        with open(filename, 'a') as output:
            # class to concept
            for (class_name, concepts) in self.class_and_concept.items():
                for concept in concepts:
                    output.write('%d\t%d\t%s\t%s\n' % (0, 0, class_name, concept))

            # <unk> to every possible concepts
            for concept in self.concepts:
                output.write('%d\t%d\t%s\t%s\n' % (0, 0, '<unk>', concept))

            # word_without_associated_class to the same word
            for word in self.word_without_associated_class:
                output.write('%d\t%d\t%s\t%s\n' % (0, 0, word, word))

            # write last line
            output.write('0')

if __name__ == '__main__':
    w2concept = W2Concept(CONCEPT_FILENAME)
    w2concept.set_word_without_associated_class('./w2class/word_without_class.txt')
    w2concept.write_w2concept_transducer('./w2concept/w2concept.fsm')

    lexicon = lex.read_lexicon_file(LEX_FILE)
    new_lexicon = w2concept.concepts.union(set(w2concept.class_and_concept.keys()))
    new_lexicon = new_lexicon.union(w2concept.word_without_associated_class)
    lexicon = lexicon.union(new_lexicon)
    lex.write_lexicon_to_file(LEX_FILE, list(lexicon))





