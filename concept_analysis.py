import pdb
import levenshtein as lev

OUTPUT_FILE = './tmp/output_test.txt'
ORIGINAL_CONTEXT_FILE = './test_grammar/concept_for_sentences.txt'

def number_of_sentences_recognized(filename):
    number_of_lines = 0
    number_of_sentences = 0
    with open(filename) as f:
        for line in f:
            # pdb.set_trace()
            number_of_lines += 1
            if len(line.strip()) != 0:
                number_of_sentences += 1

    print "Recognized %d sentences over %d" % (int(number_of_sentences), int(number_of_lines))

def analyse_edit_distance(recognized_concept_file, annotated_concept_file):
    recognized_concepts = list()
    annotated_concepts = list()

    with open(recognized_concept_file) as f:
        recognized_concepts = f.readlines()

    with open(annotated_concept_file) as f:
        annotated_concepts = f.readlines()

    # if len(recognized_concepts) != len(annotated_concepts):
    #     print "something wrong in the code!!!"
    #     return 0

    edit_distance = list()
    for i in range(len(recognized_concepts)):
        a1 = recognized_concepts[i].strip(' \n').split(' ')
        a2 = annotated_concepts[i].strip().split(' ')

        if a1[0] != '':
            distance = lev.levenshtein2(a1, a2)
            edit_distance.append(distance)
        else:
            print 'else running'
            edit_distance.append(-1)

    return edit_distance

def write_edit_distance(output_file, edit_distance):
    with open(output_file, 'w') as output:
        output.writelines('%d\n' % d for d in edit_distance)

if __name__ == '__main__':
    number_of_sentences_recognized(OUTPUT_FILE)
    edit_distance = analyse_edit_distance(OUTPUT_FILE, ORIGINAL_CONTEXT_FILE)
    write_edit_distance('./tmp/edit_distance.txt', edit_distance)
    pdb.set_trace()

    a = 2
