import re
import pdb

GRAMMAR_FSM_FILE = './grammar/grammar.fsm'
GRAMMAR_LEX_FILE = './lex/grammar_lex.txt'

def generate_grammar_lexicon(grammar_fsm_file):
    terminals = set()
    non_terminals = set()

    # special case
    non_terminals.add('SS')

    with open(grammar_fsm_file) as f:
        for line in f:
            line = line.strip()
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

if __name__ == '__main__':
    non_terminals, terminals = generate_grammar_lexicon(GRAMMAR_FSM_FILE)
    write_grammar_lex(GRAMMAR_LEX_FILE, non_terminals, terminals)
