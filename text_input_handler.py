import re

ABBREVIATIONS = ["bl.a.", "f.eks.", "d.", "ca."]
MATCH_DIGIT_WORD_REGEX = r"\d|\w"


def clean_and_split_sentences(text_input):
    sentences = split_to_sentences(text_input)
    return tokenize_and_clean_sentences(sentences)


def tokenize_and_clean_sentences(sentences):
    # for storing and returning the cleaned sentences
    sentences_cleaned = []

    for s in sentences:
        # for storing the cleaned words in a sentence
        cleaned_tokens = []

        # split sentence on " "
        tokens = s.split()

        for w in tokens:
            # check if the word is a known abbreviation
            found = False
            for a in ABBREVIATIONS:
                if w.startswith(a):  # a == w:
                    found = True  # re.search(a, w)):
                    w = a

            # check patterns
            if(re.search(r"\d+\.", w)):
                found = True

            # remove non word/digit characters from the start of the word
            while(not found and len(w) >= 1 and re.search(MATCH_DIGIT_WORD_REGEX, w[0]) == None):
                w = w[1:len(w)] if len(w) >= 1 else ""

            # if not an abbreviation, remove non word/digit characters from end of string
            while(not found and len(w) >= 1 and re.search(MATCH_DIGIT_WORD_REGEX, w[len(w)-1]) == None):
                w = w[:len(w)-1] if len(w) >= 1 else ""

            # if the word is only one character, check if word/digit
            # if(len(w) == 1 and re.search(MATCH_DIGIT_WORD_REGEX, w) == None):
            #    w = ""

            # append the cleaned word to cleaned_tokens
            cleaned_tokens.append(w)

        # print(" ".join(cleaned_tokens), "\n")

        # append the cleaned sentence to sentences_cleaned
        sentences_cleaned.append(" ".join(cleaned_tokens))

    return sentences_cleaned
    # print(s)


def split_to_sentences(text_input):
    i = 0
    sentences = []
    sen = ""
    for c in text_input:
        look_ahead_behind = text_input[i-16:i+16]
        if((c == "." or c == "?" or c == "!") and find_abbreviations(look_ahead_behind) == False):
            sentences.append(sen.strip())
            sen = ""
        else:
            sen = sen+c
        i += 1
    return sentences


def find_abbreviations(text):
    found = False

    if(re.search(r"\d+\.", text)):  # re.search(r"\d+\. [a-z|ø|å|æ]", text)
        found = True

    for a in ABBREVIATIONS:
        l = len(text)//2
        text[l-len(a):l+len(a)]
        if a in text:
            found = True
    return found
