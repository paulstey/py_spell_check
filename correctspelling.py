import os
import pandas as pd

from symspellpy.symspellpy import SymSpell, Verbosity  # import the module

DICT_FILE_PATH = "/Users/pstey/software/resources/python/frequency_dictionary_en_82_765.txt"



## maximum edit distance per dictionary precalculation
#   max_edit_distance_dictionary = 2
#   prefix_length = 7

# Example dict file 
# DICT_FILE_PATH = os.path.join(os.path.dirname(__file__), "frequency_dictionary_en_82_765.txt")


def load_dictionary(dictionary_path, max_edit_distance_dictionary = 3, prefix_length = 7):

    # create object
    sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)
    
    term_index = 0  # column of the term in the dictionary text file
    count_index = 1  # column of the term frequency in the dictionary text file
    
    if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
        print("Dictionary file not found")
        return None
    return sym_spell


def get_correction(sym_spell, input_str, max_edit_distance_lookup = 3):
    # max edit distance per lookup
    # (max_edit_distance_lookup <= max_edit_distance_dictionary)
    suggestion_verbosity = Verbosity.CLOSEST  # TOP, CLOSEST, ALL
    suggestions = sym_spell.lookup(input_str, suggestion_verbosity, max_edit_distance_lookup)
        
        # display suggestion term, term frequency, and edit distance
    # for suggestion in suggestions:
    #     print("{}, {}, {}".format(suggestion.term, suggestion.distance, suggestion.count))
    #     
    return suggestions[0].term

input_str = "wordingg"

symspell = load_dictionary(DICT_FILE_PATH)
    
get_correction(symspell, input_str)



# NOTE: We get an order-of magnitude speed up on correctly spelled words by 
# first checking if the word is in our `sym_spell._words` dictionary
def auto_correct(sym_spell, input_str, max_edit_distance_lookup = 3):
    # max edit distance per lookup
    # (max_edit_distance_lookup <= max_edit_distance_dictionary)

    if " " not in input_str:
        if input_str in sym_spell._words:
            return input_str

        suggestion_verbosity = Verbosity.CLOSEST  # TOP, CLOSEST, ALL
        suggestions = sym_spell.lookup(input_str, suggestion_verbosity, max_edit_distance_lookup)
    else:
        suggestions = sym_spell.lookup_compound(input_str, max_edit_distance_lookup)
    
    # display suggestion term, term frequency, and edit distance
    # for suggestion in suggestions:
    #     print("{}, {}, {}".format(suggestion.term, suggestion.distance, suggestion.count))
    correction = suggestions[0].term
    # print("Correct `{}` to `{}`".format(input_str, correction))
    
    return correction
    


def auto_correct_columns(sym_spell, df, cols):
    n = df.shape[0]
    for col in cols:
        for i in range(n):
            df.loc[i, col] = auto_correct(sym_spell, df.loc[i, col])
    return None 

    
    
df = pd.DataFrame({"x1": ["this is a cell", "adn this also", "and this tooo", "yep, here alos"],
                   "x2": ["the words that aer", "in this isn't", "very complexx", "krunchy"]})
                   
auto_correct_columns(symspell, df, ["x1", "x2"])


                   

