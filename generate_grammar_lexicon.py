import re
import lexicon_operation as lex
import pdb

ORIGINAL_GRAMMAR_FSM_FILE = './grammar/grammar_skeleton.fsm'
GRAMMAR_FSM_FILE = './grammar/grammar.fsm'
GRAMMAR_LEX_FILE = './lex/grammar_lex.txt' # not used in this file - Apr 22
LEX_FILE = './lex/lex_ngramsymbols.syms'

def generate_grammar_lexicon(grammar_fsm_file):
    terminals = set()
    non_terminals = set()

    # special case
    non_terminals.add('SS')

    with open(grammar_fsm_file) as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                break

            words = re.split('[ |]+', line)

            for word in words:
                if word.startswith('@'):
                    non_terminals.add(word)
                else:
                    terminals.add(word)

    # remove special case
    try:
        terminals.remove('<epsilon>')
        non_terminals.remove('<epsilon>')
    except:
        pass

    return non_terminals, terminals

def write_grammar_lex(grammar_lex_file, non_terminals, terminals):
    try:
        non_terminals.remove('')
        terminals.remove('')
    except:
        pass
    with open(grammar_lex_file, 'w') as output:
        count = 0
        # write special case
        for word in ['<epsilon>', '<unk>']:
            output.write('%s\t%d\n' % (word, count))
            count += 1

        for word in non_terminals:
            output.write('%s\t%d\n' % (word, count))
            count += 1

        for word in terminals:
            output.write('%s\t%d\n' % (word, count))
            count += 1

def set_word_without_associated_class(word_without_associated_class_filename):
    word_list = set()

    with open(word_without_associated_class_filename) as f:
        word_without_associated_class = f.read().split('\n')
        word_list = set(word_without_associated_class)

    return word_list

def write_additional_grammar_rule(original_grammar_fsm_file, word_without_associated_class):
    with open(GRAMMAR_FSM_FILE, 'w') as output:
        with open(original_grammar_fsm_file) as f:
            for line in f:
                output.write(line)

        word_without_associated_class = list(word_without_associated_class)

        l = len(word_without_associated_class)
        for i in range(0, l, 100):
            try:
                new_rule = ' | '.join([x for x in word_without_associated_class[i:(i + 99)]])
                output.write('%s %s\n' % ('Word', new_rule))
            except:
                new_rule = ' | '.join([x for x in word_without_associated_class[i:(l-1)] ])
                output.write('%s %s\n' % ('Word', new_rule))

if __name__ == '__main__':
    lexicon = lex.read_lexicon_file(LEX_FILE)
    non_terminals, terminals = generate_grammar_lexicon(ORIGINAL_GRAMMAR_FSM_FILE)

    # Write non_important words such as i also need
    # but not those word that is used to mark the appearance of concept
    # such as 'from, to, between, arrive, depart'
    word_without_associated_class = set_word_without_associated_class('./w2class/word_without_class.txt')
    non_important_words = word_without_associated_class.difference(terminals)
    write_additional_grammar_rule(ORIGINAL_GRAMMAR_FSM_FILE, non_important_words)

    # Generate new lexicon with symbols from Context-Free-Grammar
    terminals = terminals.union(lexicon)
    non_terminals = non_terminals.difference(lexicon)
    write_grammar_lex(LEX_FILE, non_terminals, terminals)
