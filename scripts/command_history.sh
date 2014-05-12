# ngramsymbols ../data/atis.hlti.train > ../lex/lex_ngramsymbols.original

cd ../

LEX_FILE=./lex/lex_ngramsymbols.syms
GRAMMAR_GRM_FILE=./grammar/grammar.fsm
GRAMMAR_BIN_FILE=./grammar/bin_grammar.bin
GRAMMAR_FSA_FILE=./grammar/grammar.fsa

CLASS_TRANSDUCER=./w2class/w2class.fst
CONCEPT_TRANSDUCER=./w2concept/w2concept.fst
FAR_FILE=./tmp/atis_train.far
FAR_TEST_FILE=./tmp/atis_test.far

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

#################
# III. Test the transducers
#################
# Test the sentences in training set & build the FSTs
# head -n 1000 ./data/atis.hlti.train | farcompilestrings -u '<unk>' -i $LEX_FILE > $FAR_FILE

# farfilter "fsmcompose - $CLASS_TRANSDUCER"<$FAR_FILE > ./tmp/result1.far
# farfilter "fsmcompose - $CONCEPT_TRANSDUCER"<./tmp/result1.far > ./tmp/result2.far
# farfilter "fsmcompose - $GRAMMAR_FSA_FILE"<./tmp/result2.far > ./tmp/result3.far

# Test the sentences in the testing set
cat ./data/atis.test | farcompilestrings -u '<unk>' -i $LEX_FILE > $FAR_TEST_FILE
farfilter "fsmcompose - $CLASS_TRANSDUCER"<$FAR_TEST_FILE > ./tmp/result_test1.far
farfilter "fsmcompose - $CONCEPT_TRANSDUCER"<./tmp/result_test1.far > ./tmp/result_test2.far
farfilter "fsmcompose - $GRAMMAR_FSA_FILE"<./tmp/result_test2.far > ./tmp/result_test3.far

farprintstrings -o $LEX_FILE ./tmp/result_test3.far > ./tmp/output.txt

python concept_analysis.py
