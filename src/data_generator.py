#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matcher as matcher
import text_input_handler as tih
import helpers as h

from pydub import AudioSegment
from pydub.utils import which


ORIG_BOOK_TEXT = open("data/text/008_7pet_sample.txt", encoding="utf-8").read()

#AudioSegment.converter = which("avlib")
if __name__ == '__main__':
    # Split the original text input to sentences, generally on periods.
    sentences = tih.clean_and_split_sentences(ORIG_BOOK_TEXT)
    # Collect STT transcribed data either locally or from cloud
    transcribed_input = h.load_data(True)
    # Convert the transcribed data to custom word objects with text, start and end time.
    transcribed_words = h.convert_transcript_to_word_objects(transcribed_input)

    # Find the position of the original text in the transcribed data using a matching algorithm
    #t = matcher.test(sentences, transcribed_words)
    t = matcher.full_sentence_matching(sentences, transcribed_words)
    # Cut audio and export the succesfully matched sentences, discard uncertain data
    audio = AudioSegment.from_file("data/audio/008_7pet.wav", format="wav")
    matcher.sort_export(t, transcribed_words, audio)
