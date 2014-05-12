# Similar to command_history, to test a grammar with few sentences

# ngramsymbols ../data/atis.hlti.train > ../lex/lex_ngramsymbols.original

cd ../

LEX_FILE=./lex/lex_ngramsymbols.syms
CONCEPT_LEX_FILE=./lex/lex_concept.lex
GRAMMAR_GRM_FILE=./grammar/grammar.fsm
GRAMMAR_BIN_FILE=./grammar/bin_grammar.bin

CLASS_TRANSDUCER=./w2class/w2class.fst
CONCEPT_TRANSDUCER=./w2concept/w2concept.fst
GRAMMAR_FSA_FILE=./grammar/grammar.fsa
TERMINAL_TRANSDUCER=./test_grammar/terminal.fst

FAR_FILE=./tmp/atis_train.far
FAR_FILE_TEST=./tmp/atis_test.far

##################
# I. Prepare the fsm
##################

# Generate lexicon
rm ./lex/lex_ngramsymbols.syms
rm ./lex/lex_ngramsymbols.original
python generate_lexicon.py
cp ./lex/lex_ngramsymbols.original ./lex/lex_ngramsymbols.syms

# Generate w2class
rm ./w2class/w2class.fsm
python generate_w2class.py

# Generate w2concept
rm ./w2concept/w2concept.fsm
python generate_w2concept.py

# Generate grammar
python generate_grammar_lexicon.py

# Generate terminal fsm
python generate_terminal.py
ngramsymbols ./data/concepts > ./lex/lex_concept.lex

#################
# II. Generate all transducers....
#################
# w2class
fsmcompile -i $LEX_FILE -o $LEX_FILE -t ./w2class/w2class.fsm > $CLASS_TRANSDUCER

# w2concept
fsmcompile -i $LEX_FILE -o $LEX_FILE -t ./w2concept/w2concept.fsm > $CONCEPT_TRANSDUCER

# Grammar
grmread -i $LEX_FILE -c $GRAMMAR_GRM_FILE > ./grammar/bin_grammar.bin
grmcfcompile -i $LEX_FILE -s Sentence -O 1 $GRAMMAR_BIN_FILE > $GRAMMAR_FSA_FILE

# Terminal FSM
fsmcompile -i $CONCEPT_LEX_FILE -o $CONCEPT_LEX_FILE -t ./test_grammar/terminal.fsm > $TERMINAL_TRANSDUCER

#################
# III. Test the transducers with the training set
#################
# head -n 1000 ./data/atis.hlti.train | farcompilestrings -u '<unk>' -i $LEX_FILE > $FAR_FILE

# farfilter "fsmcompose - $CLASS_TRANSDUCER"<$FAR_FILE > ./tmp/result1.far
# farfilter "fsmcompose - $CONCEPT_TRANSDUCER"<./tmp/result1.far > ./tmp/result2.far
# farfilter "fsmcompose - $GRAMMAR_FSA_FILE"<./tmp/result2.far > ./tmp/result3.far

# farprintstrings -i $LEX_FILE -o $LEX_FILE ./tmp/result1.far > ./tmp/result1.txt
# farprintstrings -o $LEX_FILE ./tmp/result2.far > ./tmp/result2.txt
# farprintstrings -o $LEX_FILE ./tmp/result3.far > ./tmp/output.txt

# python concept_analysis.py

######################
# IV. Test the transducer with the test set
######################
cat ./test_grammar/sentences.txt | farcompilestrings -u '<unk>' -i $LEX_FILE > $FAR_FILE_TEST
# head -n 10 ./test_grammar/sentences.txt | farcompilestrings -u '<unk>' -i $LEX_FILE > $FAR_FILE_TEST

farfilter "fsmcompose - $CLASS_TRANSDUCER"<$FAR_FILE_TEST > ./tmp/result1_test.far
farfilter "fsmcompose - $CONCEPT_TRANSDUCER"<./tmp/result1_test.far > ./tmp/result2_test.far
farfilter "fsmcompose - $GRAMMAR_FSA_FILE"<./tmp/result2_test.far > ./tmp/result3_test.far

farprintstrings -i $LEX_FILE -o $LEX_FILE ./tmp/result1_test.far > ./tmp/result1_test.txt
farprintstrings -o $LEX_FILE ./tmp/result2_test.far > ./tmp/result2_test.txt
farprintstrings -o $LEX_FILE ./tmp/result3_test.far > ./tmp/result3_test.txt

FAR_GRAMMAR_TEST=./tmp/atis_grammar_test.far
cat ./tmp/result3_test.txt | farcompilestrings -u 'null' -i $CONCEPT_LEX_FILE > $FAR_GRAMMAR_TEST
farprintstrings -o $CONCEPT_LEX_FILE $FAR_GRAMMAR_TEST > ./tmp/output_test.txt

python concept_analysis.py




