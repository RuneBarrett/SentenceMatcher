import pickle
import objects as obj


def convert_transcript_to_word_objects(transcribed_input):
    output = []
    # print(inspect.getmembers(transcribed_input))
    for result in transcribed_input.results:
        for w in result.alternatives[0].words:
            output.append(obj.word(w.word.lower(),
                                   w.start_time.seconds + w.start_time.nanos*1e-9,
                                   w.end_time.seconds + w.end_time.nanos*1e-9,
                                   w.confidence))
    # for obj in output:
        # obj.printer()
    return output


def load_data(use_local_data):
    """Collects data either from the cloud or locally depending on use_local_data"""

    # pretranscribed sample data
    if use_local_data:
        # ORIG_BOOK_TEXT = open("data/text/008_7pet_sample.txt", "r").read()
        with open("data/obj_storage/response_obj.pkl", 'rb') as inp:
            response = pickle.load(inp)

    # use google cloud STT
    else:
        print("use STT API call")  # call transcibe_async.py
        # ORIG_BOOK_TEXT = None
        response = None

    return response
