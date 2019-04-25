#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matcher as matcher
import text_input_handler as tih
import helpers as h
import os
import time

import pydub

ORIG_BOOK_TEXT = open("data/text/Syv år for PET.txt", encoding="utf-8").read()

if __name__ == '__main__':

    # Split the original text input to sentences, generally on periods.
    sentences = tih.clean_and_split_sentences(ORIG_BOOK_TEXT)
    sentence_num = 0

    for section, filename in enumerate(os.listdir("data/obj_storage")):
        print("--- Processing: ", filename)
        transcribed_input = h.load_data(True, filename)
        # Convert the transcribed data to custom word objects with text, start and end time.
        transcribed_words = h.convert_transcript_to_word_objects(
            transcribed_input)

        # Find the position of the original text in the transcribed data using a matching algorithm
        matched_sentences, sen_num = matcher.full_sentence_matching(
            sentences[sentence_num:], transcribed_words)
        sentence_num += sen_num

        matched_sentences = matcher.full_sentence_full_text_matcher(
            sentences, transcribed_input)

        # Cut audio and export the succesfully matched sentences, discard uncertain data
        audio_filename = "data/audio/7pet_flac/" + \
            filename.replace("pkl", "mp3.flac")
        print(audio_filename)
        #pydub.AudioSegment.converter = "C:\\Users\\runeb\\Documents\\ffmpeg-20190425\\bin\\ffmpeg.exe"

        audio = pydub.AudioSegment.from_file(audio_filename, format="flac")
        matcher.sort_export(matched_sentences,
                            transcribed_words, audio, section)
