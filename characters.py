# Up here, we import additional functionality that we'll need to do this demo.

# The Natural Language Processing Toolkit (NLTK) is a Python library with a lot
# of really powerful tools for textual analysis.
from nltk import pos_tag, word_tokenize, download, chunk, Tree
# collections is a Python library with the super-awesome Counter, which takes a
# list and returns a dictionary that tallies up how many times each value appears.
# For example, ['red', 'red', 'rose'] would become [('red',  2), ('rose': 1)}.
from collections import Counter
# PrettyPrinter will make our final output easier to read in the console.
import pprint

download('punkt')
download('averaged_perceptron_tagger')
download('maxent_ne_chunker')
download('words')


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
    # counts = dict(Counter(proper_nouns).most_common(top_num))
    proper_nouns_only = [pn[0] for pn in proper_nouns]
    pn_to_tuple = {pn[0]: pn for pn in proper_nouns}
    counts = dict(Counter(proper_nouns_only))
    return {k: [v, pn_to_tuple[k][1]] for k, v in sorted(counts.items(), key=lambda item: item[1])}


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
        tag = []
        name = ""
        if is_nnp(tagged_text[i]):
            name += tagged_text[i][0].lower() + " "
            tag.append(tagged_text[i][1])
            j = i + 1
            while j < len(tagged_text):
                if is_nnp(tagged_text[j]):
                    name += tagged_text[j][0].lower()
                    tag.append(tagged_text[j][1])
                    j += 1
                    continue
                if is_pos(tagged_text[j]) and is_nnp(tagged_text[j+1]):
                    name = name.strip() + tagged_text[j][0].lower() + " " + tagged_text[j+1][0].lower() + " "
                    tag.append(tagged_text[j][1])
                    tag.append(tagged_text[j+1][1])
                    j += 2
                    continue
                if is_cc(tagged_text[j]) and is_nnp(tagged_text[j+1]):
                    name += tagged_text[j][0].lower() + " " + tagged_text[j+1][0].lower() + " "
                    tag.append(tagged_text[j][1])
                    tag.append(tagged_text[j+1][1])
                    j += 2
                    continue
                break
            if i >= 1 and is_dt(tagged_text[i - 1]):
                name = tagged_text[i - 1][0].lower() + " " + name + " "
                tag = [tagged_text[j - 1][1]] + tag

            if '-' not in name:
                proper_nouns.append([name.strip(), tag])
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
tagged = tagging(b)
d = find_proper_nouns_v2(tagged)
e = summarize_text(d, 100)

# top_10 = []
limit = 20
for idx, (k,v) in enumerate(sorted(e.items(), key=lambda item: item[1], reverse=True), start=1):
    if idx == limit + 1:
        break
    print(f"{idx}. {k}, {v}")
    # if len(top_10) < 10:
    #     top_10.append(k)
    # else:
    #     for t in top_10:
    #         t_split = t.split()
    #         k_split = k.split()
    #
    #         for tt in t_split:
    #             if

#
# print(tagged)
entities = chunk.ne_chunk(tagged)
# print(type(entities))
# for k, v in entities.items():
#     print(k, v)
# print(entities)


ROOT = 'ROOT'

def getNodes(parent):
    persons = []
    for node in parent:
        if type(node) is Tree:
            if node.label() == ROOT:
                pass
            #     print("======== Sentence =========")
            #     print("Sentence:", " ".join(node.leaves()))
            else:
                # print("Label:", node.label())
                if node.label() == "PERSON":
                    persons.append((' '.join([n[0] for n in node.leaves()]), [n[1] for n in node.leaves()]))
                    # print("Leaves:", node.leaves())

            getNodes(node)
        # else:
        #     print("Word:", node)
    return persons

persons = getNodes(entities)

persons_only = [pn[0] for pn in persons]
pn_to_tuple = {pn[0]: pn for pn in persons}
counts = dict(Counter(persons_only))
res = {k: [v, pn_to_tuple[k][1]] for k, v in sorted(counts.items(), key=lambda item: item[1])}
print("----------------------------")

for idx, (k,v) in enumerate(sorted(res.items(), key=lambda item: item[1], reverse=True), start=1):
    if idx == limit + 1:
        break
    print(f"{idx}. {k}, {v}")
#
# harry [1212, ['NNP']]
# ron [361, ['NNP']]
# hagrid [354, ['NNP']]
# hermione [178, ['NNP']]
# snape [145, ['NNP']]
# dudley [118, ['NNP']]
# dumbledore [111, ['NNP']]
# neville [110, ['NNP']]
# malfoy [107, ['NNP']]
# uncle vernon [99, ['NNP', 'NNP']]
# professor mcgonagall [91, ['NNP', 'NNP']]
# quirrell [88, ['NNP']]
# gryffindor [57, ['NNP']]
# hogwarts [54, ['NNP']]
# the dursleys [48, ['NNP', 'NNP']]
# potter [46, ['NNP']]
# wood [46, ['NNP']]
# aunt petunia [43, ['NNP', 'NNP']]
# filch [43, ['NNP']]
# well [40, ['NNP']]
#
#
# Harry [1244, ['NNP']]
# Ron [411, ['NNP']]
# Hagrid [286, ['NNP']]
# Hermione [230, ['NNP']]
# Snape [140, ['NNP']]
# Dudley [125, ['NNP']]
# Uncle Vernon [104, ['NNP', 'NNP']]
# Neville [93, ['NNP']]
# Dumbledore [81, ['NNP']]
# Malfoy [63, ['NNP']]
# Quirrell [54, ['NNP']]
# Aunt Petunia [50, ['NNP', 'NNP']]
# Wood [49, ['NN']]
# Filch [44, ['NNP']]
# Professor McGonagall [41, ['NNP', 'NNP']]
# Potter [36, ['NNP']]
# Percy [31, ['NNP']]
# Mr. Dursley [29, ['NNP', 'NNP']]
# Harry Potter [25, ['NNP', 'NNP']]
# Slytherin [25, ['NNP']]