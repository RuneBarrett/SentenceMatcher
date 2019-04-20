import pickle
import json
import inspect
from google.protobuf.json_format import MessageToJson


def main():
    with open("data/obj_storage/response_obj.pkl", 'rb') as input:
        response = pickle.load(input)
    print_it(response)

    #data = json.dumps(MessageToJson(response))
    #with open('data.json', 'w') as outfile:
    #    json.dump(data, outfile)


def print_it(response):
    # print(inspect.getmembers(response))
    # return
    for result in response.results:
        alternative = result.alternatives[0]
        print(u'Transcript: {}'.format(alternative.transcript))
        print('Confidence: {}'.format(alternative.confidence))

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            conf = word_info.confidence
            print('Word: {}, start_time: {}, end_time: {}, conf: {}'.format(
                word,
                start_time.seconds + start_time.nanos * 1e-9,
                end_time.seconds + end_time.nanos * 1e-9,
                conf))
        break


main()
