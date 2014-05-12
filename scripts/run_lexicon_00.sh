cd ../

rm ./lex/lex_ngramsymbols.syms
rm ./lex/lex_ngramsymbols.original

python generate_lexicon.py

cp ./lex/lex_ngramsymbols.original ./lex/lex_ngramsymbols.syms