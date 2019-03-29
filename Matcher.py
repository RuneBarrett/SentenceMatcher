"""
Usage: python matcher.py gs://abook_data/008_7pet.wav
"""
import pickle

USE_SAMPLE_DATA = True
#origBookText, response = "", None
#currentPos, sentenceCount = 0, 0


def main():
    """The main process of the program"""

    # Collects data either through the cloud or locally
    orig_book_text, response = load_data()
    #origBookText = data[0]
    #response = data[1]
    # this is too simple, but works for now (splits on abbreviations for example)
    sentences = orig_book_text.split(". ")
    for sen in sentences:
        print(sen.strip(), "\n")


# def compareSentence(origSen, transSen):
#     print("not yet")


# def getOrigSentence():  # Manual sentence splitter "skeleton"
#     global currentPos, origBookText
#     origBookText = origBookText[currentPos:len(origBookText)]
#     endPos = origBookText.find(".")
#     sentence = origBookText[currentPos:endPos]
#     currentPos = endPos
#     return sentence


def load_data():
    """Collects data either from the cloud or locally depending on USE_SAMPLE_DATA"""
    #global response, origBookText
    # pretranscribed sample data
    if USE_SAMPLE_DATA:
        orig_book_text = open("data/text/008_7pet_sample.txt", "r").read()
        with open("data/obj_storage/response_obj.pkl", 'rb') as inp:
            response = pickle.load(inp)
    # use google cloud STT
    else:
        print("cloud STT")  # call transcibe_async.py
        orig_book_text = None
        response = None

    return orig_book_text, response


main()  # python "hack" to use a main func in the top of the file
