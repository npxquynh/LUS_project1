import pdb

class TestGrammar():
    sentences = list()
    class_for_sentences = list()
    concept_for_sentences = list()

    def __init__(self, test_file, output_folder):
        self.read_test_file(test_file)
        self.write_test_data_to_file(output_folder)

    def read_test_file(self, filename):
        temp_word = list()
        temp_class = list()
        temp_concept = list()

        with open(filename) as f:
            for line in f:
                line = line.strip()

                if len(line) == 0:
                    # Error handling
                    if len(temp_word) == len(temp_class) == len(temp_concept):
                        self.sentences.append(' '.join(temp_word))
                        self.class_for_sentences.append(' '.join(temp_class))
                        self.concept_for_sentences.append(' '.join(temp_concept))

                    temp_word = list()
                    temp_class = list()
                    temp_concept = list()
                else:
                    words = line.split(' ')
                    temp_word.append(words[0])
                    temp_class.append(words[1])
                    temp_concept.append(words[2])

    def write_test_data_to_file(self, output_folder):
        with open('%s/sentences.txt' % output_folder, 'w') as output:
            output.writelines('%s\n' % l for l in self.sentences)

        with open('%s/class_for_sentences.txt' % output_folder, 'w') as output:
            output.writelines('%s\n' % l for l in self.class_for_sentences)

        with open('%s/concept_for_sentences.txt' % output_folder, 'w') as output:
            output.writelines('%s\n' % l for l in self.concept_for_sentences)

if __name__ == '__main__':
    test_grammar = TestGrammar('./data/atis.test', './test_grammar')



