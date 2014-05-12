def read_concept_file(filename):
    concepts = set()

    with open(filename) as f:
        for line in f:
            concepts.add(line.strip())

    return concepts

##########
# May 5, 2014: Do not need it, we can use fsmcompilestrings with another
# lexicon, unknown symbols as 'null', and everything is okie
##########
# def generate_terminal_fsm(concepts, output_filename):
#     with open(output_filename, 'w') as output:
#         # write special case: everything will not in the concept_list will be null
#         # output.write('%d\t%d\t%s\t%s\n' % (0, 0, '<epsilon>', 'null'))
#         # output.write('%d\t%d\t%s\t%s\n' % (0, 0, '<unk>', 'null'))

#         for concept in concepts:
#             output.write('%d\t%d\t%s\t%s\n' % (0, 0, concept, concept))

#         # final state
#         # output.write('%d\n' % 0)

if __name__ == '__main__':
    concepts = read_concept_file('./data/concepts')

