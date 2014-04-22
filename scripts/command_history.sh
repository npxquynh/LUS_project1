ngramsymbols ../data/atis.hlti.train > ../lex/lex_ngramsymbols.original

./run_w2class_02.sh

./run_w2concept_03.sh

./run_fsm_01.sh

./test.sh
