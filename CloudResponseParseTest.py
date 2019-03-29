import pickle
import json
from google.protobuf.json_format import MessageToJson


def main():
    with open("data/response_obj.pkl", 'rb') as input:
        response = pickle.load(input)
    print_it(response)

    data = json.dumps(MessageToJson(response))
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)


def print_it(response):
    for result in response.results:
        alternative = result.alternatives[0]
        print(u'Transcript: {}'.format(alternative.transcript))
        print('Confidence: {}'.format(alternative.confidence))

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            print('Word: {}, start_time: {}, end_time: {}'.format(
                word,
                start_time.seconds + start_time.nanos * 1e-9,
                end_time.seconds + end_time.nanos * 1e-9))


main()
