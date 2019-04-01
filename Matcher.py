"""
Usage: python matcher.py gs://abook_data/008_7pet.wav
"""
import pickle
import re

USE_SAMPLE_DATA = True
ORIG_BOOK_TEXT = open("data/text/008_7pet_sample.txt", "r").read()
SAMPLE_ABBR = ["11. ", "bl.a."]


def main():
    """The main process of the program"""

    # Collects data either through the cloud or locally

    response = load_data()

    # sentences = ORIG_BOOK_TEXT.split(".")
    sentences = split_and_clean_data()
    # for sen in sentences:
    #    print(sen, "\n")

    remove_non_word_digit(sentences)


def remove_non_word_digit(sentences):
    sentences_corrected = []
    for s in sentences:
        sentence = s.split()
        sen_corrected = []
        for w in sentence:
            while(len(w) > 1 and re.search("\d|\w", w[0]) == None):
                w = w[1:len(w)]
            while(len(w) > 1 and re.search("\d|\w", w[len(w)-1]) == None):
                w = w[:len(w)-1]
            if(len(w) == 1):
                if(re.search("\d|\w", w) == None):
                    w = ""
            sen_corrected.append(w)
            #print(w, len(w))
        print(" ".join(sen_corrected), "\n")
        # print(s)


def split_and_clean_data():
    i = 0
    sentences = []
    sen = ""
    for c in ORIG_BOOK_TEXT:
        look_ahead_behind = ORIG_BOOK_TEXT[i-4:i+4]
        sen = sen+c
        if((c == "." or c == "?" or c == "!") and find_abbreviations(look_ahead_behind) == None):
            sentences.append(sen.strip())
            sen = ""
        i += 1
    return sentences


def find_abbreviations(text):
    r = re.search("\d*\. [a-z|ø|å|æ]", text)
    #print(r,  " - ", text, "\n")
    return r


def load_data():
    """Collects data either from the cloud or locally depending on USE_SAMPLE_DATA"""

    # pretranscribed sample data
    if USE_SAMPLE_DATA:
        # ORIG_BOOK_TEXT = open("data/text/008_7pet_sample.txt", "r").read()
        with open("data/obj_storage/response_obj.pkl", 'rb') as inp:
            response = pickle.load(inp)

    # use google cloud STT
    else:
        print("use STT API call")  # call transcibe_async.py
        # ORIG_BOOK_TEXT = None
        response = None

    return response


main()  # python "hack" to use a main func in the top of the file
