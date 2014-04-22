cd ../
LEX_FILE='./lex/lex_ngramsymbols.syms'

fsmcompile -i $LEX_FILE -o $LEX_FILE -t ./w2class/w2class.fsm > ./w2class/w2class.fst
fsmcompile -i $LEX_FILE -o $LEX_FILE -t ./w2concept/w2concept.fsm > ./w2concept/w2concept.fst

fsmcompose ./fsm/0001.fsm ./w2class/w2class.fst > ./result1/0001.fst
fsmdraw -i $LEX_FILE -o $LEX_FILE ./result1/0001.fst | dot -Teps > ./pic1/0001.ps

fsmcompose ./result1/0001.fst ./w2concept/w2concept.fst > ./result2/0001.fst
fsmdraw -i $LEX_FILE -o $LEX_FILE ./result2/0001.fst | dot -Teps > ./pic2/0001.ps

