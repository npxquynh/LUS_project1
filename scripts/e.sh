# run after d.sh, to visualize stuffs

LEX_FILE=./lex/lex_ngramsymbols.syms

# Preparation
cd ../
rm ./result1/*
rm ./result2/*
rm ./result3/*
rm ./pic_grammar/*
rm ./pic1/*
rm ./pic2/*


#######################
# IV. Show result
#######################

cd ./result2
rm -rf
farsplit ../tmp/result2.far
cd ../result3
farsplit ../tmp/result3.far
cd ../

# b. Visualize a grammar
# fsmdraw -i $LEX_FILE $GRAMMAR_FSA_FILE | dot -Teps > ./pic_grammar/grammar_fsa.ps

ls ./result2/*.fsm | xargs -n1 basename > ./result2/fst_filename.txt
for file in $(cat ./result2/fst_filename.txt)
do
    fsmdraw -i $LEX_FILE -o $LEX_FILE ./result2/$file | dot -Teps > ./pic2/${file%%.*}.ps
done

ls ./result3/*.fsm | xargs -n1 basename > ./result3/fst_filename.txt
for file in $(cat ./result3/fst_filename.txt)
do
    fsmdraw -i $LEX_FILE -o $LEX_FILE ./result3/$file | dot -Teps > ./pic_grammar/${file%%.*}.ps
done
