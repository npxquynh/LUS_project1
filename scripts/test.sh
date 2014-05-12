cd ../
LEX_FILE=./lex/lex_ngramsymbols.syms

GRAMMAR_GRM_FILE=./grammar/grammar.fsm
GRAMMAR_BIN_FILE=./grammar/bin_grammar.bin
GRAMMAR_FSA_FILE=./grammar/grammar.fsa

CLASS_TRANSDUCER=./w2class/w2class.fst
CONCEPT_TRANSDUCER=./w2concept/w2concept.fst
FAR_FILE=./tmp/atis_train.far

# I. Prepare all the transducer
# w2class
fsmcompile -i $LEX_FILE -o $LEX_FILE -t ./w2class/w2class.fsm > ./w2class/w2class.fst

# w2concept
fsmcompile -i $LEX_FILE -o $LEX_FILE -t ./w2concept/w2concept.fsm > ./w2concept/w2concept.fst

# Grammar
grmread -i $LEX_FILE -c $GRAMMAR_GRM_FILE > ./grammar/bin_grammar.bin
grmcfcompile -i $LEX_FILE -s Sentence -O 1 $GRAMMAR_BIN_FILE > $GRAMMAR_FSA_FILE

# II. Using farfilter
farfilter "fsmcompose - $CLASS_TRANSDUCER"<$FAR_FILE > ./tmp/result1.far
farfilter "fsmcompose - $CONCEPT_TRANSDUCER"<./tmp/result1.far > ./tmp/result2.far
farfilter "fsmcompose - $GRAMMAR_FSA_FILE"<./tmp/result2.far > ./tmp/result3.far

# IIa. try to print the result
# farprintstrings -i $LEX_FILE -o $LEX_FILE $FAR_FILE
# farprintstrings -i $LEX_FILE -o $LEX_FILE ./tmp/result1.far
farprintstrings -i $LEX_FILE -o $LEX_FILE ./tmp/result1.far > ./tmp/result1.txt
farprintstrings -o $LEX_FILE ./tmp/result2.far > ./tmp/result2.txt
farprintstrings -o $LEX_FILE ./tmp/result3.far > ./tmp/output.txt

python concept_analysis.py

# # III. Specific version
# # Composing FSTs
# fsmcompose ./fsm/0001.fsm ./w2class/w2class.fst > ./result1/0001.fst
# fsmdraw -i $LEX_FILE -o $LEX_FILE ./result1/0001.fst | dot -Teps > ./pic1/0001.ps

# fsmcompose ./result1/0001.fst ./w2concept/w2concept.fst > ./result2/0001.fst
# fsmdraw -i $LEX_FILE -o $LEX_FILE ./result2/0001.fst | dot -Teps > ./pic2/0001.ps

# fsmcompose ./result2/0001.fst $GRAMMAR_FSA_FILE > ./result3/0001b.fst
# fsmdraw -i $LEX_FILE -o $LEX_FILE ./result3/0001b.fst | dot -Teps > ./pic_grammar/0001b.ps

