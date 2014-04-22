# generating fsa for the text
farcompilestrings -i lex2.txt prova2.txt > prova2.far
fsmdraw -i lex2.txt prova2.far | dot -Tps > prova2.ps
farsplit prova2.far

#compiling the transducer
grmread -i lex2.txt rules2.txt > grammar2.bin
fsmdraw -i lex2.txt -o lex2.txt grammar2.bin | dot -Tps > grammar2.ps

#compiling the acceptor
grmcfcompile -i lex2.txt -s Sentence -O 1 grammar2.bin > grammar2.fsa
fsmdraw -i lex2.txt grammar2.fsa | dot -Teps > grammar_fsa2.ps

# recognize sentence with this grammar2
fsmcompose 0001.fsm grammar2.fsa > 0001b.fsa
fsmdraw -i lex2.txt 0001b.fsa | dot -Teps > sentence_compose_grammar.ps