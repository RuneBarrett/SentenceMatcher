"""
Example usage:
    python transcribe_async.py data/audio/kap1_7pet_29.wav
    python transcribe_async.py gs://abook_data/008_7pet.wav
"""

import pickle
import argparse
import io
from google.cloud import speech_v1p1beta1 as speech
#from google.cloud.speech import enums
#from google.cloud.speech import types

CLIENT = speech.SpeechClient()

# config variables
LANGUAGE_CODE = "da-DK"
HERTZ = 44100
ENCODING = speech.enums.RecognitionConfig.AudioEncoding.LINEAR16


def transcribe_file(speech_file):
    """Transcribe the given audio file under one minute asynchronously."""
    # load audio content
    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    # create audio object from file
    # pylint: disable=no-member
    audio = speech.types.RecognitionAudio(content=content)

    # create a request configuration
    config = get_config()

    # start the transcription operation
    operation = CLIENT.long_running_recognize(
        config, audio)

    # wait for the response
    print('Waiting for operation to complete...')
    response = operation.result(timeout=900)
    handle_results(response)


def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""

    # create audio object from uri
    # pylint: disable=no-member
    audio = speech.types.RecognitionAudio(uri=gcs_uri)

    # create a request configuration
    config = get_config()

    # start the transcription operation
    operation = CLIENT.long_running_recognize(config, audio)

    # wait for the response
    print('Waiting for operation to complete...')
    response = operation.result(timeout=900)
    handle_results(response)

    # save the python response object to the disk for later use
    #save_object(response, "response_obj.pkl")


def handle_results(response):
    """#handles a result object for testing/printing"""
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        print('Confidence: {}'.format(result.alternatives[0].confidence))
    save_object(response, "response_obj.pkl")


def get_config():
    """#configures a request for the STT API"""
    # pylint: disable=no-member
    return speech.types.RecognitionConfig(
        encoding=ENCODING,
        sample_rate_hertz=HERTZ,
        language_code=LANGUAGE_CODE,
        enable_word_time_offsets=True,
        enable_word_confidence=True)


def save_object(obj, filename):
    """Saves the response object to a file"""
    with open("data/obj_storage/"+filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    PARSER.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    ARGS = PARSER.parse_args()
    if ARGS.path.startswith('gs://'):
        transcribe_gcs(ARGS.path)
    else:
        transcribe_file(ARGS.path)
