import numpy as np
import pickle
import objects as obj
import transcribe_async as ta


def convert_transcript_to_word_objects(transcribed_input):
    output = []
    # print(inspect.getmembers(transcribed_input))
    for result in transcribed_input.results:
        for w in result.alternatives[0].words:
            output.append(obj.word(w.word.lower(),
                                   w.start_time.seconds + w.start_time.nanos*1e-9,
                                   w.end_time.seconds + w.end_time.nanos*1e-9,
                                   w.confidence))
    return output


def load_data(foldername, use_local_data=True, obj_name="response_obj.pkl", ):
    """Collects data either from the cloud or locally depending on use_local_data"""
    print("loading", obj_name)
    # pretranscribed sample data
    if use_local_data:
        with open("data/obj_storage/"+foldername+"/"+obj_name, 'rb') as inp:
            response = pickle.load(inp)

    # collect data from google cloud STT
    else:
        print("Calling STT API")
        ta.transcribe_batch("abook_data", "7pet_wav")
        response = None

    return response


def levenshtein_ratio_and_distance(s, t, ratio_calc=True):
    """ levenshtein_ratio_and_distance:
        Calculates levenshtein distance between two strings.
        If ratio_calc = True, the function computes the
        levenshtein distance ratio of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    # Initialize matrix of zeros
    rows = len(s)+1
    cols = len(t)+1
    distance = np.zeros((rows, cols), dtype=int)

    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, rows):
        for k in range(1, cols):
            distance[i][0] = i
            distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                # If the characters are the same in the two strings in a given position [i,j] then the cost is 0
                cost = 0
            else:
                # In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
                # the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
                if ratio_calc == True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                     # Cost of insertions
                                     distance[row][col-1] + 1,
                                     distance[row-1][col-1] + cost)     # Cost of substitutions
    if ratio_calc == True:
        # Computation of the Levenshtein Distance Ratio
        Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
        return Ratio
    else:
        # print(distance) # Uncomment if you want to see the matrix showing how the algorithm computes the cost of deletions,
        # insertions and/or substitutions
        # This is the minimum number of edits needed to convert string a to string b
        return "The strings are {} edits away".format(distance[row][col])
