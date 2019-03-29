import pickle

useSampleData = True
origBookText, response = None, None
currentPos = 0
sentenceCount = 0


def main():
    loadData()
    #sentenceCount = origBookText.count(".") + 1
    #print(sentenceCount, getOrigSentence())
    sentences = origBookText.split(". ")
    for s in sentences:
        print(s.strip(), "\n")


def getOrigSentence():
    global currentPos, origBookText
    origBookText = origBookText[currentPos:len(origBookText)]
    endPos = origBookText.find(".")
    sentence = origBookText[currentPos:endPos]
    currentPos = endPos
    return sentence


def loadData():
    global response, origBookText
    if useSampleData:  # pretranscribed sample data
        origBookText = open("data/008_7pet_sample.txt", "r").read()
        with open("data/response_obj.pkl", 'rb') as input:
            response = pickle.load(input)
    else:  # use google cloud STT
        print("cloud STT")


main()
