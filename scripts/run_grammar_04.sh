cd ../

python generate_grammar_lexicon.py


GRAMMAR_LEX_FILE=./lex/grammar_lex.txt
GRAMMAR_GRM_FILE=./grammar/grammar.fsm
GRAMMAR_BIN_FILE=./grammar/bin_grammar.bin
GRAMMAR_FSA_FILE=./grammar/grammar.fsa

grmread -i $GRAMMAR_LEX_FILE -c $GRAMMAR_GRM_FILE > ./grammar/bin_grammar.bin
fsmdraw -i $GRAMMAR_LEX_FILE -o $GRAMMAR_LEX_FILE $GRAMMAR_BIN_FILE | dot -Teps > ./pic_grammar/grammar_bin.ps

grmcfcompile -i $GRAMMAR_LEX_FILE -s SS -O 1 $GRAMMAR_BIN_FILE > $GRAMMAR_FSA_FILE
fsmdraw -i $GRAMMAR_LEX_FILE $GRAMMAR_FSA_FILE | dot -Teps > ./pic_grammar/grammar_fsa.ps

LEX_FILE='./lex/lex_ngramsymbols.syms'

fsmcompose ./result2/0001.fst $GRAMMAR_BIN_FILE > ./result3/0001a.fst
fsmcompose ./result2/0001.fst $GRAMMAR_FSA_FILE > ./result3/0001b.fst
fsmdraw -i $LEX_FILE -o $GRAMMAR_LEX_FILE ./result3/0001a.fst | dot -Teps > ./pic_grammar/0001a.ps
fsmdraw -i $LEX_FILE -o $GRAMMAR_LEX_FILE ./result3/0001b.fst | dot -Teps > ./pic_grammar/0001b.ps

grmcfapproximate -i lex3.txt -s E -o lex3_new.txt cfg3.bin > input3_new.txt