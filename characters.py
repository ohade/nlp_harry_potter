# Up here, we import additional functionality that we'll need to do this demo.

# The Natural Language Processing Toolkit (NLTK) is a Python library with a lot
# of really powerful tools for textual analysis.
from nltk import pos_tag, word_tokenize, download
# collections is a Python library with the super-awesome Counter, which takes a
# list and returns a dictionary that tallies up how many times each value appears.
# For example, ['red', 'red', 'rose'] would become [('red',  2), ('rose': 1)}.
from collections import Counter
# PrettyPrinter will make our final output easier to read in the console.
import pprint

download('punkt')
download('averaged_perceptron_tagger')


def read_text():
    '''
    This function reads the text into python from a text file.
    When you read in your own file, replace 'corpus/hp1.txt' with the path
    to your file.
    '''
    with open('Harry_Potter_and_the_Sorcerer_v2.txt', 'r') as f:
        book = f.read()
    f.close()
    return book

def text_tokenize(book):
    '''
    This function splits words and puctuation in the block of text created in
    the 'read_text' function into one giant list where each item is a word or
    punctuation.  For example, "Harry hung back for a last word with Harry and
    Hermione." becomes ['Harry', 'hung', 'back', 'for', 'a', 'last', 'word',
    'with', 'Harry', 'and', 'Hermione', '.']
    '''
    tokenize = word_tokenize(book)
    return tokenize

def tagging(tokenize):
    '''
    This function takes the tokenized text created
    by the text_tokenize function and tags each word with a code for the part of speech it represents
    using NLTK's algorithm.  So, it changes the tokenized output:
    ['Harry', 'hung', 'back', 'for', 'a', 'last', 'word',
    'with', 'Ron', 'and', 'Hermione', '.']
    - TO -
    [('Harry', 'NNP'),
    ('hung', 'VBD'), ('back', 'RP'), ('for', 'IN'), ('a', 'DT'), ('last', 'JJ'),
    ('word', 'NN'), ('with', 'IN'), ('Ron', 'NNP'), ('and', 'CC'),
    ('Hermione', 'NNP'), ('.', '.')]
    '''
    tagged_text = pos_tag(tokenize)
    return tagged_text


def find_proper_nouns(tagged_text):
    '''
    This function takes in the tagged text from the tagging function and Returns
    a list of words that were tagged as proper nouns.  It does this by looking
    at the second value in each word/tag pair - e.g. ('Harry', 'NNP') and determining
    if is is equal to 'NNP'.
    There are a lot of characters in these novels who are referred to with two
    proper nouns, like 'Professor Quirell', 'Mrs. Weasley', or 'Uncle Vernon',
    and any character can be called by their full name (e.g. 'Hermione Granger').
    So, if the second value IS equal to 'NNP', we check the second value of the
    next word - if it is also equal to 'NNP', we string the two words together
    and add them to the proper_nouns list.
    If the second value ISN'T equal to 'NNP', we append (add) only the first
    word to the proper_nouns list.
    As we add nouns to the list, we put them all in lower case - otherwise, our
    program won't know that 'HARRY' is the same thing for our purposes as 'Harry'.
    '''
    proper_nouns = []
    i = 0
    while i < len(tagged_text):

        if is_nnp(tagged_text[i]):
            if is_nnp(tagged_text[i+1]):
                if tagged_text[i + 2][1] == 'POS' and tagged_text[i + 3][1] == 'NNP':
                    proper_nouns.append(" ".join([tagged_text[i][0].lower(), tagged_text[i+1][0].lower(), tagged_text[i+2][0].lower(), tagged_text[i+3][0].lower()]))
                    i += 2
                else:
                    proper_nouns.append(" ".join([tagged_text[i][0].lower(), tagged_text[i+1][0].lower()]))
                i+=1 # extra increment added to the i counter to skip the next word
            elif tagged_text[i-1][1] == 'DT': # 'the'
                if tagged_text[i+1][1] == 'POS' and is_nnp(tagged_text[i + 2]):
                    i += 2
                else:
                    # proper_nouns.append(" ".join([tagged_text[i][0].lower(), tagged_text[i + 1][0].lower()]))
                    proper_nouns.append(tagged_text[i-1][0].lower() + " " + tagged_text[i][0].lower())
            else:
                if tagged_text[i + 1][1] == 'POS' and is_nnp(tagged_text[i + 2]):
                    i += 2
                else:
                    proper_nouns.append(tagged_text[i][0].lower())
        i+=1 # increment the i counter
    return proper_nouns


def summarize_text(proper_nouns, top_num):
    '''
    This function takes the proper_nouns from the list created by the
    find_proper_nouns function and counts the instances of each.  For this demo,
    we are using the most_common method that comes with the Counter.
    '''
    counts = dict(Counter(proper_nouns).most_common(top_num))
    # counts = dict(Counter(proper_nouns))
    return {k: v for k, v in sorted(counts.items(), key=lambda item: item[1])}


def is_nnp(curr_tagged_text):
    return curr_tagged_text[1] == 'NNP' and curr_tagged_text[0].upper() != curr_tagged_text[0]


def is_pos(curr_tagged_text):
    return curr_tagged_text[1] == 'POS'


def is_cc(curr_tagged_text):
    return curr_tagged_text[1] == 'CC'


def is_dt(curr_tagged_text):
    return curr_tagged_text[1] == 'DT'


def find_proper_nouns_v2(tagged_text):
    '''
    This function takes in the tagged text from the tagging function and Returns
    a list of words that were tagged as proper nouns.  It does this by looking
    at the second value in each word/tag pair - e.g. ('Harry', 'NNP') and determining
    if is is equal to 'NNP'.
    There are a lot of characters in these novels who are referred to with two
    proper nouns, like 'Professor Quirell', 'Mrs. Weasley', or 'Uncle Vernon',
    and any character can be called by their full name (e.g. 'Hermione Granger').
    So, if the second value IS equal to 'NNP', we check the second value of the
    next word - if it is also equal to 'NNP', we string the two words together
    and add them to the proper_nouns list.
    If the second value ISN'T equal to 'NNP', we append (add) only the first
    word to the proper_nouns list.
    As we add nouns to the list, we put them all in lower case - otherwise, our
    program won't know that 'HARRY' is the same thing for our purposes as 'Harry'.
    '''
    proper_nouns = []
    i = 0
    while i < len(tagged_text):
        name = ""
        if is_nnp(tagged_text[i]):
            name += tagged_text[i][0].lower() + " "
            j = i + 1
            while j < len(tagged_text):
                if is_nnp(tagged_text[j]):
                    name += tagged_text[j][0].lower()
                    j += 1
                    continue
                if is_pos(tagged_text[j]) and is_nnp(tagged_text[j+1]):
                    name = name.strip() + tagged_text[j][0].lower() + " " + tagged_text[j+1][0].lower() + " "
                    j += 2
                    continue
                if is_cc(tagged_text[j]) and is_nnp(tagged_text[j+1]):
                    name += tagged_text[j][0].lower() + " " + tagged_text[j + 1][0].lower() + " "
                    j += 2
                    continue
                break
            if i >= 1 and is_dt(tagged_text[i - 1]):
                name = tagged_text[i - 1][0].lower() + " " + name + " "
            proper_nouns.append(name.strip())
            i = j
        i += 1  # increment the i counter
    return proper_nouns

# if nnp then can follow by nnp/pos/cc
# nnp
# nnp nnp
# dt nnp
# dt nnp nnp
# dt nnp pos nnp
# nnp pos nnp
# nnp cc nnp nnp

# This is where we call all of our functions and pass what they return to the
# next function
a = read_text()
b = text_tokenize(a)
c = tagging(b)
d = find_proper_nouns_v2(c)
e = summarize_text(d, 100)

for k,v in sorted(e.items(), key=lambda item: item[1], reverse=True):
    print(k, v)