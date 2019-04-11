#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import pickle
import re
from difflib import SequenceMatcher
#from pydub import AudioSegment
import objects as obj
#import helpers
# from pydub.playback import play

import text_input_handler as t_inp_handler

#USE_SAMPLE_DATA = True
#ORIG_BOOK_TEXT = open("data/text/008_7pet_sample.txt", encoding="utf-8").read()
ABBREVIATIONS = ["bl.a.", "f.eks.", "d.", "ca."]
MATCH_DIGIT_WORD_REGEX = r"\d|\w"

# SAMPLE_ABBR = ["11. ", "bl.a."]


# def main():
#     """The main process of the program"""

#     # Split the original text input to sentences, generally on periods.
#     sentences = t_inp_handler.clean_and_split_sentences(ORIG_BOOK_TEXT)

#     # Collect STT transcribed data either locally or from cloud
#     transcribed_input = load_data()
#     # Convert the transcribed data to custom word objects with text, start and end time.
#     transcribed_words = helpers.convert_transcript_to_word_objects(
#         transcribed_input)

#     # Find the position of the original text in the transcribed data using a matching algorithm
#     t = test(sentences, transcribed_words)

#     # Cut audio and export the succesfully matched sentences, discard uncertain data
#     audio = AudioSegment.from_file("data/audio/008_7pet.wav", format="wav")
#     sort_export(t, transcribed_words, audio)


def sort_export(matched_sentences, transcribed_words, audio):
    print("exporting audio")
    for j, sen in enumerate(matched_sentences):
        w_s = transcribed_words[sen.s_index]
        if sen.e_index > len(transcribed_words):
            sen.e_index = len(transcribed_words)-1
        w_e = transcribed_words[sen.e_index]

        start_end_char_amount = int(len(sen.sen)*0.08)
        if (start_end_char_amount < 5):
            start_end_char_amount = 5

        print(sen.sen[:start_end_char_amount].lower().strip(), "/",
              sen.t_sen[:start_end_char_amount].strip(), " - ",
              sen.sen[-start_end_char_amount:].lower().strip(), "/",
              sen.t_sen[-start_end_char_amount-1:].strip())

        sim_s = sim(sen.sen[:start_end_char_amount].lower().strip(),
                    sen.t_sen[:start_end_char_amount].strip())
        sim_e = sim(sen.sen[-start_end_char_amount:].lower().strip(),
                    sen.t_sen[-start_end_char_amount-1:].strip())
        mean = (sim_s+sim_e)/2
        if(sim_s > 0.7 and sim_e > 0.7):
            print(w_s.s_time*1000, w_e.e_time*1000,
                  "sim:", sen.similarity,
                  "start:", sim_s,
                  "end:", sim_e,
                  "mean:", mean)
            s_time = w_s.s_time*1000+400 if w_s.s_time > 0 else w_s.s_time*1000
            e_time = w_e.e_time*1000-400
            audio[s_time:e_time].export(
                "data/audio/output/{}_{}-{}{}".format("%04d" % j, "%07.1f" % w_s.s_time, "%07.1f" % w_e.e_time, ".mp3"), format="mp3")
        else:
            print("SKIPPED si:", sen.similarity, "s:", sim_s, "e:", sim_e)
        print("{}\n{}".format(
            sen.sen, sen.t_sen), "\n --------------------")


def full_sentence_matching(sentences, t_words):
    next_startpoint, cur_startpoint, LOOK_AHEAD_BEHIND = 0, 0, 10
    sentences_final = []

    # loop through all sentences in the original text input
    for sen_i, orig_sen in enumerate(sentences):
        cur_sen_str, best_match = ""
        i = -LOOK_AHEAD_BEHIND
        best_i_e, best_i_s, best_sim = 0, 0, 0.0

        # As the transcription may not contain the same amount of words as the original sentence, try to find the best full sentence match by
        # adding/removing words in the beginning and the end of the transcribed sentence
        while i <= LOOK_AHEAD_BEHIND:
            # ---------------- Find best end of sentence
            cur_startpoint = next_startpoint  # set the first index of the current sentence
            trans_sen_section = t_words[cur_startpoint:cur_startpoint +  # the expected full sentence taken from the transcribed words list
                                        len(orig_sen.split())+i]
            sentence_holder_str = ""
            for a in trans_sen_section:
                sentence_holder_str += a.word+" "

            similarity = sim(orig_sen, sentence_holder_str)
            if(similarity >= best_sim):
                best_sim = similarity
                best_match = "Original: {}\nBest Match: {} \n\nSimilarity: {}".format(
                    orig_sen, sentence_holder_str, similarity)
                best_i_e = i

            # ---------------- Find best start of sentence
            best_sim = 0.0

            i += 1  # increment look ahead/behind index

        print("-------- SENTENCE {} ---------".format(sen_i))
    return sentences_final


def test(sentences, t_sentences):
    LOOK_AHEAD_BEHIND = 8
    next_startpoint = 0
    cur_startpoint = 0
    sentences_final = []
    for sen_i, s in enumerate(sentences):

        print("-------- SENTENCE {} ---------".format(sen_i))
        str = ""
        i = -LOOK_AHEAD_BEHIND
        best_match = ""
        best_str = ""
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
                best_str = str

            # print(similarity, i)
            i += 1
        print("Startpos: {} Endpos: {}".format(next_startpoint,
                                               cur_startpoint + len(s.split()) + best_i))

        next_startpoint = cur_startpoint + len(s.split()) + best_i

        i = -LOOK_AHEAD_BEHIND
        #best_sim = 0.0
        best_i_s = 0

        # find best start of sentence
        while cur_startpoint > LOOK_AHEAD_BEHIND and i <= LOOK_AHEAD_BEHIND:
            arr = t_sentences[cur_startpoint +
                              i: cur_startpoint + len(s.split()) + best_i]
            str = ""
            for a in arr:
                str += a.word+" "

            # print("i_s = {}: {}".format(i, str))

            similarity = sim(s, str)
            if(similarity >= best_sim):
                best_sim = similarity
                best_match = "Original: {}\nBest Match: {} \n\nSimilarity: {}".format(
                    s, str, similarity)
                best_i_s = i
                best_str = str

            # print(similarity, i)
            i += 1

        str2 = ""
        # print(best_i_s-plus_minus, best_i+plus_minus)
        # for b in t_sentences[cur_startpoint-LOOK_AHEAD_BEHIND: next_startpoint+LOOK_AHEAD_BEHIND]:
        for b in t_sentences[cur_startpoint: next_startpoint]:
            str2 += b.word+" "
        print("\n{}\n\nMoved start pos amount: {} \nMoved end pos amount: {}".format(
            best_match, best_i_s, best_i))
        print("\nTranscribed +- {}:\n{}\n ------------------------------ \n".format(LOOK_AHEAD_BEHIND, str2))

        sentences_final.append(obj.matched_sentence(
            s, best_str, best_sim, cur_startpoint+best_i_s, next_startpoint))
    return sentences_final


def sim(w1, w2):
    return SequenceMatcher(None, w1.lower(), w2.lower()).ratio()


# def convert_transcript_to_word_objects(transcribed_input):
#     output = []
#     # print(inspect.getmembers(transcribed_input))
#     for result in transcribed_input.results:
#         for w in result.alternatives[0].words:
#             output.append(obj.word(w.word.lower(),
#                                    w.start_time.seconds + w.start_time.nanos*1e-9,
#                                    w.end_time.seconds + w.end_time.nanos*1e-9,
#                                    w.confidence))
#     # for obj in output:
#         # obj.printer()
#     return output


# class word:
#     def __init__(self, word, s_time, e_time, conf):
#         self.word = word
#         self.s_time = s_time
#         self.e_time = e_time
#         self.conf = conf

#     def printer(self):
#         print('Word: {}, s_time: {}, e_time: {}, conf: {}'.format(
#             self.word, self.s_time, self.e_time, self.conf))


# class sentence_final:
#     def __init__(self, sen, t_sen, similarity, s_index, e_index):
#         self.sen = sen
#         self.t_sen = t_sen
#         self.s_index = s_index
#         self.e_index = e_index
#         self.similarity = similarity


# def load_data():
#     """Collects data either from the cloud or locally depending on USE_SAMPLE_DATA"""

#     # pretranscribed sample data
#     if USE_SAMPLE_DATA:
#         # ORIG_BOOK_TEXT = open("data/text/008_7pet_sample.txt", "r").read()
#         with open("data/obj_storage/response_obj.pkl", 'rb') as inp:
#             response = pickle.load(inp)

#     # use google cloud STT
#     else:
#         print("use STT API call")  # call transcibe_async.py
#         # ORIG_BOOK_TEXT = None
#         response = None

#     return response


# main()  # python "hack" to use a main func in the top of the file
