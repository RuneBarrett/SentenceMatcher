import pickle

useSampleData = True
origBookText, response = "", None
currentPos, sentenceCount = 0, 0


def main():
    # Collects data either through the cloud or locally
    loadData()
    # this is too simple, but works for now (splits on abbreviations for example)
    sentences = origBookText.split(". ")
    for s in sentences:
        print(s.strip(), "\n")


def compareSentence(origSen, transSen):
    print("")


def getOrigSentence():  # Manual sentence splitter "skeleton"
    global currentPos, origBookText
    origBookText = origBookText[currentPos:len(origBookText)]
    endPos = origBookText.find(".")
    sentence = origBookText[currentPos:endPos]
    currentPos = endPos
    return sentence


def loadData():  # Collects data either from the cloud or locally depending on useSampleData
    global response, origBookText
    # pretranscribed sample data
    if useSampleData:
        origBookText = open("data/008_7pet_sample.txt", "r").read()
        with open("data/response_obj.pkl", 'rb') as input:
            response = pickle.load(input)
    # use google cloud STT
    else:
        print("cloud STT")  # call transcibe_async.py


main()  # python "hack" to use a main func
