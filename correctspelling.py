import os

from symspellpy.symspellpy import SymSpell, Verbosity  # import the module

## maximum edit distance per dictionary precalculation
#   max_edit_distance_dictionary = 2
#   prefix_length = 7

# Example dict file 
# dict_file_path = os.path.join(os.path.dirname(__file__), "frequency_dictionary_en_82_765.txt")

dict_file_path = "/Users/pstey/software/resources/python/frequency_dictionary_en_82_765.txt"

def load_dictionary(dictionary_path, max_edit_distance_dictionary = 3, prefix_length = 7):

    # create object
    sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
    
    term_index = 0  # column of the term in the dictionary text file
    count_index = 1  # column of the term frequency in the dictionary text file
    
    if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
        print("Dictionary file not found")
        return None
    return sym_spell


def get_correction(sym_spell, input_term, max_edit_distance_lookup = 2):
    # max edit distance per lookup
    # (max_edit_distance_lookup <= max_edit_distance_dictionary)
    suggestion_verbosity = Verbosity.CLOSEST  # TOP, CLOSEST, ALL
    suggestions = sym_spell.lookup(input_term, suggestion_verbosity, max_edit_distance_lookup)
        
        # display suggestion term, term frequency, and edit distance
    # for suggestion in suggestions:
    #     print("{}, {}, {}".format(suggestion.term, suggestion.distance, suggestion.count))
    #     
    return suggestions[0].term

input_term = "wordingg"

symspell = load_dictionary(dict_file_path)
    
get_correction(symspell, input_term)



# NOTE: We get an order-of magnitude speed up on correctly spelled words by 
# first checking if the word is in our `sym_spell._words` dictionary
def get_correction2(sym_spell, input_term, max_edit_distance_lookup = 2):
    # max edit distance per lookup
    # (max_edit_distance_lookup <= max_edit_distance_dictionary)
    if input_term in sym_spell._words:
        return input_term

    suggestion_verbosity = Verbosity.CLOSEST  # TOP, CLOSEST, ALL
    suggestions = sym_spell.lookup(input_term, suggestion_verbosity, max_edit_distance_lookup)

    # display suggestion term, term frequency, and edit distance
    # for suggestion in suggestions:
    #     print("{}, {}, {}".format(suggestion.term, suggestion.distance, suggestion.count))
    #     
    return suggestions[0].term
