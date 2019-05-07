#!/usr/bin/env python
# -*- coding: utf-8 -*-

from difflib import SequenceMatcher
import objects as obj
import helpers as h
import time
import csv


def full_sentence_matching(sentences, t_words):
    """  As the transcription may not contain the same amount of words as the original sentence, this method tries to find the best sentence match by
         adding/removing words in the beginning and the end, and comparing the full sentences with a difference algorithm
    """
    cur_endpoint, cur_startpoint, LOOK_AHEAD_BEHIND = -1, 0, 20
    sentences_final = []

    # loop through all sentences in the original text input
    for sen_i, orig_sen in enumerate(sentences):
        # if(cur_endpoint >= len(t_words)):
        #     print("{}, {}".format("no match, move on", sen_i))
        #     time.sleep(4)
        #     break
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
        cur_endpoint = cur_startpoint + len(orig_sen.split())-1 + best_i_e
        best_sim = 0

        while i <= LOOK_AHEAD_BEHIND and cur_startpoint > LOOK_AHEAD_BEHIND:
            trans_sen_section = t_words[cur_startpoint + i: cur_endpoint]
            best_i_s, best_sim, best_match = join_and_compare_sentences(
                trans_sen_section, orig_sen, best_sim, i, best_i_s, best_match, sen_i)
            i += 1

        # Add the best match to the list of matched sentences
        sentences_final.append(obj.matched_sentence(
            orig_sen, best_match, best_sim, cur_startpoint+best_i_s, cur_endpoint))
        print("{} - {} - {}".format(len(t_words), cur_startpoint, cur_endpoint))

        # print the results during execution for analysis
        if(cur_endpoint <= len(t_words) and cur_startpoint < cur_endpoint and len(best_match) > 0):
            full_sentence_matcher_LOGGER(sen_i, cur_startpoint, cur_endpoint, best_sim, best_i_s,
                                         best_i_e, t_words, LOOK_AHEAD_BEHIND, orig_sen, best_match)
        else:
            print("{}, {}".format("no match 2, move on", sen_i))
            # time.sleep(4)
            return sentences_final, sen_i+1

        # sentence_holder_str = " ".join(a.word for a in trans_sen_section)
        # or abs(len(best_match)-len(sentence_holder_str) > 30)
        # if(best_match == "" or):
        #     print("{}, {}".format("no match 2, move on", sen_i))
        #     time.sleep(4)
        #     break
    return sentences_final, sen_i


def join_and_compare_sentences(trans_sen_section, orig_sen, best_sim, i, best_i, best_match, sen_i):
    # sentence_holder_str = ""
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


def full_sentence_full_text_matcher(sentences, transcribed_input):
    # Traverse the full text document to find the best match for each sentence
    return None


def sim(w1, w2):
    # Pythons seqencematcher fails for strings longer than 200 characters
    if(len(w1) >= 200):
        o_str1, t_str1, o_str2, t_str2 = w1[:199], w2[:199], w1[200:], w2[200:]
        similarity = (SequenceMatcher(None, o_str1.lower(), t_str1.lower()).ratio() + SequenceMatcher(None, o_str2.lower(),
                                                                                                      t_str2.lower()).ratio()) / 2
    else:
        similarity = SequenceMatcher(None, w1.lower(), w2.lower()).ratio()

    return similarity


def sort_export(matched_sentences, transcribed_words, audio, section):
    print("exporting")
    csv_lines = []
    for j, sen in enumerate(matched_sentences):
        if(sen.s_index < len(transcribed_words)):
            print(sen.s_index, len(transcribed_words))
            w_s = transcribed_words[sen.s_index]
            if sen.e_index > len(transcribed_words):
                sen.e_index = len(transcribed_words)-1
            w_e = transcribed_words[sen.e_index-1]

            start_end_char_amount = int(len(sen.sen)*0.06)
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

                s_time = w_s.s_time*1000+300 if w_s.s_time > 0 else w_s.s_time*1000
                # if (w_e.e_time-w_e.s_time) >= 0.1 else w_e.e_time*1000
                e_time = w_e.e_time*1000+600
                print(w_s.word, w_e.word, w_e.e_time-w_e.s_time)
                name = "{}_{}_{}-{}".format("%03d" % (section+2), "%04d" %
                                            j, "%06.1f" % w_s.s_time, "%06.1f" % w_e.e_time)
                a_out = audio[s_time:e_time]
                print(a_out.duration_seconds)
                if(a_out.duration_seconds <= 12.0):
                    a_out.export(
                        "data/audio/output/{}_{}_{}-{}{}".format("%03d" % (section+2), "%04d" % j, "%06.1f" % w_s.s_time, "%06.1f" % w_e.e_time, ".wav"), format="wav")
                    csv_lines.append([name + "|" + sen.sen + "|" + sen.t_sen])
                # row = ['name', 'test']
                # with open('output.csv', 'a') as csvFile:
                #     writer = csv.writer(csvFile)
                #     writer.writerow(row)
                # csvFile.close()

            else:
                print("SKIPPED si:", sen.similarity, "s:", sim_s, "e:", sim_e)
            print("{}\n{}".format(
                sen.sen, sen.t_sen), "\n --------------------")
        else:
            print("s_pos to big")

    return csv_lines


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
    for b in t_words[max(0, cur_startpoint-int(LOOK_AHEAD_BEHIND/2)): cur_endpoint+int(LOOK_AHEAD_BEHIND/2)]:
        str2 += b.word+" "
    print("\nOriginal: \n{}\nBest Match: \n{} \n".format(orig_sen, best_match))

    print("\nTranscribed +- {}:\n{}\n---------------------------------------------- \n".format(
        int(LOOK_AHEAD_BEHIND/2), str2))
