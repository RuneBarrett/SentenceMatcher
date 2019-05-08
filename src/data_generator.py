#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matcher as matcher
import text_input_handler as tih
import helpers as h
import os
import time
import csv
import pydub
start_time = time.time()

# Load text version of the book to be processed
ORIG_BOOK_TEXT = open("data/in_text/SyvaarforPET.txt",
                      encoding="utf-8").read()
# ORIG_BOOK_TEXT = open("data/in_text/JyttefraMarketing.txt",
#                       encoding="utf-8").read()

# The name of the folders where the original audiobook files are (used by exporter), as well as the google STT response objects
ABOOK_FOLDER_NAME = "7pet_flac"
#ABOOK_FOLDER_NAME = "jytte"


# This number can be used to modify the numbering of the output files (useful if combining output from multiple books)
OUTPUT_SEC_NUM = 2

if __name__ == '__main__':

    # Split the original text input to sentences, generally on periods.
    sentences = tih.clean_and_split_sentences(ORIG_BOOK_TEXT)
    sentence_num = 0
    # input("WARNING: Press any key to delete output.csv and continue...")
    if os.path.exists("data/output.csv"):
        os.remove("data/output.csv")
    csv_lines = []

    for section, filename in enumerate(sorted(os.listdir("data/obj_storage/"+ABOOK_FOLDER_NAME))):
        print("--- Processing: ", filename)
        transcribed_input = h.load_data(ABOOK_FOLDER_NAME, True, filename)
        # Convert the transcribed data to custom word objects with text, start and end time.
        transcribed_words = h.convert_transcript_to_word_objects(
            transcribed_input)

        # Find the position of the original text in the transcribed data using a matching algorithm
        matched_sentences, sen_num = matcher.full_sentence_matching(
            sentences[sentence_num:], transcribed_words)
        sentence_num += sen_num

        # Load the original audio for the current section
        audio_filename = "data/in_audio/"+ABOOK_FOLDER_NAME+"/" + \
            filename.replace("pkl", "mp3.flac")
        audio = pydub.AudioSegment.from_file(audio_filename, format="flac")

        # Cut audio -> export the succesfully matched sentences -> add metadata to the csv
        csv_lines += matcher.sort_export(matched_sentences,
                                         transcribed_words, audio, section, OUTPUT_SEC_NUM)
        # TEST only run X seconds for for testing
        if(time.time() - start_time > 12):
            break

    with open('data/output/output.csv', 'w', newline="", encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csv_lines)

    print("Done. Created {} entries in {} seconds".format(
        len(csv_lines), "%01.2f" % (time.time() - start_time)))
    csvFile.close()
