cd ../fsm/

LEX_FILE='../lex/lex_ngramsymbols.syms'

rm *

head -n 4 ../data/atis.hlti.train | farcompilestrings -u '<unk>' -i $LEX_FILE > ../tmp/atis_train.far
# farcompilestrings -i ../lex/lex_ngramsymbols.syms ../data/atis.hlti.train -f const_input_indexed > atis_train.far
farsplit ../tmp/atis_train.far

fsmdraw -i $LEX_FILE 0001.fsm | dot -Teps > ../pic0/0001.ps