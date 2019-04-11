class word:
    def __init__(self, word, s_time, e_time, conf):
        self.word = word
        self.s_time = s_time
        self.e_time = e_time
        self.conf = conf

    def printer(self):
        print('Word: {}, s_time: {}, e_time: {}, conf: {}'.format(
            self.word, self.s_time, self.e_time, self.conf))


class matched_sentence:
    def __init__(self, sen, t_sen, similarity, s_index, e_index):
        self.sen = sen
        self.t_sen = t_sen
        self.s_index = s_index
        self.e_index = e_index
        self.similarity = similarity
