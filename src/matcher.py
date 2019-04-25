#!/usr/bin/env python
# -*- coding: utf-8 -*-

from difflib import SequenceMatcher
import objects as obj
import helpers as h
import time


def full_sentence_matching(sentences, t_words):
    """  As the transcription may not contain the same amount of words as the original sentence, this method tries to find the best sentence match by
         adding/removing words in the beginning and the end, and comparing the full sentences with a difference algorithm
    """
    cur_endpoint, cur_startpoint, LOOK_AHEAD_BEHIND = -1, 0, 15
    sentences_final = []

    # loop through all sentences in the original text input
    for sen_i, orig_sen in enumerate(sentences):

        best_i_e, best_i_s, best_sim, best_match = 0, 0, -1.0, ""

        # ---------- Find best end of sentence ----------
        # set the first index of the current sentence to the last index of previous sentence+1
        cur_startpoint = cur_endpoint+1
        i = -LOOK_AHEAD_BEHIND
        while i <= LOOK_AHEAD_BEHIND:
            trans_sen_section = t_words[cur_startpoint:cur_startpoint +  # the full sentence with the current lookahead taken from the transcribed words list
                                        (len(orig_sen.split())-1)+i]
            # Join words to sentence, compare with the original, update "best" variables through join_and_compare_sentences
            best_i_e, best_sim, best_match = join_and_compare_sentences(
                trans_sen_section, orig_sen, best_sim, i, best_i_e, best_match, sen_i)
            i += 1

        # ---------- Find best start of sentence ----------
        i = -LOOK_AHEAD_BEHIND
        cur_endpoint = cur_startpoint + len(orig_sen.split())-1 + best_i_e-1
        if(cur_endpoint > len(t_words)):
            break
        while i <= LOOK_AHEAD_BEHIND and cur_startpoint > LOOK_AHEAD_BEHIND:
            trans_sen_section = t_words[cur_startpoint + i: cur_endpoint]
            best_i_s, best_sim, best_match = join_and_compare_sentences(
                trans_sen_section, orig_sen, best_sim, i, best_i_s, best_match, sen_i)
            i += 1

        # Add the best match to the list of matched sentences
        sentences_final.append(obj.matched_sentence(
            orig_sen, best_match, best_sim, cur_startpoint+best_i_s, cur_endpoint))
        print("{} - {}".format(len(t_words), cur_endpoint))
        # print the results during execution for analysis
        full_sentence_matcher_LOGGER(sen_i, cur_startpoint, cur_endpoint, best_sim, best_i_s,
                                     best_i_e, t_words, LOOK_AHEAD_BEHIND, orig_sen, best_match)

        #sentence_holder_str = " ".join(a.word for a in trans_sen_section)
        # or abs(len(best_match)-len(sentence_holder_str) > 30)
        if(best_match == "" or cur_endpoint > len(t_words)):
            print("no match")
            break
            time.sleep(2)
    return sentences_final, sen_i


def join_and_compare_sentences(trans_sen_section, orig_sen, best_sim, i, best_i, best_match, sen_i):
    #sentence_holder_str = ""
    # for a in trans_sen_section:  # convert the transcribed array section to a string
    #    sentence_holder_str += a.word+" "
    # sentence_holder_str = sentence_holder_str.strip()  # remove trailing " "

    sentence_holder_str = " ".join(a.word for a in trans_sen_section)
    similarity = sim(orig_sen, sentence_holder_str)
    # if(sen_i == 27):
    #    print(sentence_holder_str, similarity, "\n")
    if(similarity >= best_sim):
        best_sim = similarity
        best_match = sentence_holder_str.strip()
        best_i = i  # -1
    return best_i, best_sim, best_match


def test(sentences, t_sentences):
    LOOK_AHEAD_BEHIND = 40
    cur_endpoint = 0
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
            cur_startpoint = cur_endpoint
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
        print("Startpos: {} Endpos: {}".format(cur_endpoint,
                                               cur_startpoint + len(s.split()) + best_i))

        cur_endpoint = cur_startpoint + len(s.split()) + best_i

        i = -LOOK_AHEAD_BEHIND
        # best_sim = 0.0
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
        # for b in t_sentences[cur_startpoint-LOOK_AHEAD_BEHIND: cur_endpoint+LOOK_AHEAD_BEHIND]:
        for b in t_sentences[cur_startpoint: cur_endpoint]:
            str2 += b.word+" "
        print("\n{}\n\nMoved start pos amount: {} \nMoved end pos amount: {}".format(
            best_match, best_i_s, best_i))
        print("\nTranscribed +- {}:\n{}\n ------------------------------ \n".format(LOOK_AHEAD_BEHIND, str2))

        sentences_final.append(obj.matched_sentence(
            s, best_str, best_sim, cur_startpoint+best_i_s, cur_endpoint))
    return sentences_final


def sim(w1, w2):
    # Pythons seqencematcher fails for strings longer than 200 characters
    if(len(w1) >= 200):
        o_str1, t_str1, o_str2, t_str2 = w1[:199], w2[:199], w1[200:], w2[200:]
        similarity = SequenceMatcher(None, o_str1.lower(), t_str1.lower()).ratio() + SequenceMatcher(None, o_str2.lower(),
                                                                                                     t_str2.lower()).ratio() / 2
    else:
        similarity = SequenceMatcher(None, w1.lower(), w2.lower()).ratio()

    return similarity


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

        if(sim_s > 0.7 and sim_e > 0.7):  # and w_e.e_time > w_s.s_time
            print(w_s.s_time*1000, w_e.e_time*1000,
                  "sim:", sen.similarity,
                  "start:", sim_s,
                  "end:", sim_e)

            s_time = w_s.s_time*1000+200 if w_s.s_time > 0 else w_s.s_time*1000
            # if (w_e.e_time-w_e.s_time) >= 0.1 else w_e.e_time*1000
            e_time = w_e.e_time*1000+500
            print(w_s.word, w_e.word, w_e.e_time-w_e.s_time)
            audio[s_time:e_time].export(
                "data/audio/output/{}_{}-{}{}".format("%04d" % j, "%07.1f" % w_s.s_time, "%07.1f" % w_e.e_time, ".mp3"), format="mp3")
        else:
            print("SKIPPED si:", sen.similarity, "s:", sim_s, "e:", sim_e)
        print("{}\n{}".format(
            sen.sen, sen.t_sen), "\n --------------------")


def full_sentence_matcher_LOGGER(sen_i, cur_startpoint, cur_endpoint, best_sim, best_i_s, best_i_e, t_words, LOOK_AHEAD_BEHIND, orig_sen, best_match):
    print("---------------- SENTENCE {} -----------------".format(sen_i))
    print("Startpos: {} Endpos: {}".format(
        cur_startpoint, cur_endpoint))
    if(len(t_words) > cur_endpoint):
        print("StartTime: {} EndTime: {}".format(
            t_words[cur_startpoint].s_time, t_words[cur_endpoint].e_time))
    print("Similarity: {} \ns_pos correction: {} \ne_pos correction: {} ".format(
        best_sim, best_i_s, best_i_e))
    str2 = ""
    for b in t_words[cur_startpoint-int(LOOK_AHEAD_BEHIND/2): cur_endpoint+int(LOOK_AHEAD_BEHIND/2)]:
        str2 += b.word+" "
    print("\nOriginal: \n{}\nBest Match: \n{} \n".format(orig_sen, best_match))

    print("\nTranscribed +- {}:\n{}\n---------------------------------------------- \n".format(
        int(LOOK_AHEAD_BEHIND/2), str2))
