"""
Usage: python matcher.py gs://abook_data/008_7pet.wav
"""
import pickle

USE_SAMPLE_DATA = True


def main():
    """The main process of the program"""

    # Collects data either through the cloud or locally
    orig_book_text, response = load_data()

    # this is too simple, but works for now (splits on abbreviations for example)
    sentences = orig_book_text.split(". ")
    for sen in sentences:
        print(sen.strip(), "\n")


def load_data():
    """Collects data either from the cloud or locally depending on USE_SAMPLE_DATA"""

    # pretranscribed sample data
    if USE_SAMPLE_DATA:
        orig_book_text = open("data/text/008_7pet_sample.txt", "r").read()
        with open("data/obj_storage/response_obj.pkl", 'rb') as inp:
            response = pickle.load(inp)

    # use google cloud STT
    else:
        print("use STT API call")  # call transcibe_async.py
        orig_book_text = None
        response = None

    return orig_book_text, response


main()  # python "hack" to use a main func in the top of the file
