cd ../

LEX_FILE='./lex/lex_ngramsymbols.syms'

rm ./lex/lex_ngramsymbols.syms
cp ./lex/lex_ngramsymbols.original ./lex/lex_ngramsymbols.syms

rm ./w2class/w2class.fsm
python generate_w2class.py