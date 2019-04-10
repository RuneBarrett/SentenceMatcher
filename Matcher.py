#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage: python matcher.py gs://abook_data/008_7pet.wav
"""
import pickle
import re
from difflib import SequenceMatcher


import text_input_handler as t_inp_handler

USE_SAMPLE_DATA = True
ORIG_BOOK_TEXT = open("data/text/008_7pet_sample.txt", encoding="utf-8").read()
ABBREVIATIONS = ["bl.a.", "f.eks.", "d.", "ca."]
MATCH_DIGIT_WORD_REGEX = r"\d|\w"
# SAMPLE_ABBR = ["11. ", "bl.a."]


def main():
    """The main process of the program"""

    # Collect STT data either through the cloud or locally

    sentences = t_inp_handler.clean_and_split_sentences(ORIG_BOOK_TEXT)
    transcribed_input = load_data()
    transcribed_words = convert_transcript_to_word_objects(transcribed_input)
    test(sentences, transcribed_words)
    return

    matching(sentences, transcribed_words)

    # for sen in sentences:
    #    print(sen, "\n")


def matching(sentences, t_sentences):
    t_i = 0

    for s in sentences:
        temp_i = 0
        temp_str = ""
        for w in s.split():
            temp_str += t_sentences[temp_i].word + " "
            temp_i += 1
        print("", s, "\n", temp_str)

        # for w in s.split():
        #     s = sim(w, t_sen[t_i].word)
        #     print(w, t_sen[t_i].word, s)
        #     t_i += 1

        #     if(s < 0.9):
        #         print("p")
        # print(" ".join((s.split()[-5:])))

        i_t = 0
        i_s = 0
        done = False
        sen = s.split()
        while(not done):
            if(sim(sen[i_s], t_sentences[i_t].word) > 0.9):
                print(sen[i_s], t_sentences[i_t].word,
                      sim(sen[i_s], t_sentences[i_t].word))
                i_t += 1
                i_s += 1
            else:
                print("problem")
                done = True
        break

    return None


def test(sentences, t_sentences):
    LOOK_AHEAD_BEHIND = 10
    next_startpoint = 0
    cur_startpoint = 0
    for sen_i, s in enumerate(sentences):

        print("-------- SENTENCE {} ---------".format(sen_i))
        str = ""
        i = -LOOK_AHEAD_BEHIND
        best_match = ""
        best_i = 0
        best_sim = 0.0

        while i <= LOOK_AHEAD_BEHIND:
            cur_startpoint = next_startpoint
            arr = t_sentences[cur_startpoint:cur_startpoint +
                              len(s.split())+i]
            str = ""
            for a in arr:
                str += a.word+" "

            similarity = sim(s, str)
            if(similarity >= best_sim):
                best_sim = similarity
                best_match = "Original: {}\nBest Match: {} \n\nSimilarity: {}".format(
                    s, str, similarity)
                best_i = i

            #print(similarity, i)
            i += 1
        print("Startpos: {} Endpos: {}".format(next_startpoint,
                                               cur_startpoint + len(s.split()) + best_i))

        next_startpoint = cur_startpoint + len(s.split()) + best_i

        i = -LOOK_AHEAD_BEHIND
        best_sim = 0.0
        best_i_s = 0

        # find best start of sentence
        while cur_startpoint > LOOK_AHEAD_BEHIND and i <= LOOK_AHEAD_BEHIND:
            arr = t_sentences[cur_startpoint +
                              i: cur_startpoint + len(s.split()) + best_i]
            str = ""
            for a in arr:
                str += a.word+" "

            #print("i_s = {}: {}".format(i, str))

            similarity = sim(s, str)
            if(similarity >= best_sim):
                best_sim = similarity
                best_match = "Original: {}\nBest Match: {} \n\nSimilarity: {}".format(
                    s, str, similarity)
                best_i_s = i

            #print(similarity, i)
            i += 1

        str2 = ""
        #print(best_i_s-plus_minus, best_i+plus_minus)
        for b in t_sentences[cur_startpoint-LOOK_AHEAD_BEHIND: next_startpoint+LOOK_AHEAD_BEHIND]:
            str2 += b.word+" "
        print("\n{}\n\nMoved start pos amount: {} \nMoved end pos amount: {}".format(
            best_match, best_i_s, best_i))
        print("\nTranscribed +- {}:\n{}\n ------------------------------ \n".format(LOOK_AHEAD_BEHIND, str2))


def sim(w1, w2):
    return SequenceMatcher(None, w1, w2).ratio()


def convert_transcript_to_word_objects(transcribed_input):
    output = []
    # print(inspect.getmembers(transcribed_input))
    for result in transcribed_input.results:
        for w in result.alternatives[0].words:
            output.append(word(w.word,
                               w.start_time.seconds + w.start_time.nanos*1e-9,
                               w.end_time.seconds + w.end_time.nanos*1e-9,
                               w.confidence))
    # for obj in output:
        # obj.printer()
    return output


class word:
    def __init__(self, word, s_time, e_time, conf):
        self.word = word
        self.s_time = s_time
        self.e_time = e_time
        self.conf = conf

    def printer(self):
        print('Word: {}, s_time: {}, e_time: {}, conf: {}'.format(
            self.word, self.s_time, self.e_time, self.conf))


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
