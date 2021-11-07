import csv
from collections import Counter, defaultdict
from scipy import spatial


class vector_embeddings:

    def __init__(self):
        self.term_document_matrix = Counter()
        self.vocab = None
        self.matrix = {}
        self.playl = Counter()
        self.cleaned_words = []
        self.cleanesdffd_words = []
        self.play_names = None

    def load_vocab_file(self):
        with open('Shakespeare_vocab.txt') as f:
            lines = f.read().split('\n')
        self.vocab = set(lines)

    def load_play_name_list(self):
        with open('Shakespeare_play_names.txt') as f:
            lines = f.read().split('\n')
        self.play_names = set(lines)

    def clean(self, word):
        return ''.join([x for x in word.lower() if x.isalnum()])

    def read_csv(self):
        term_frequency = defaultdict(lambda: 0)
        with open("ShakespearePlays_text.csv", "r") as f:
            # load csv
            reader = csv.reader(f, delimiter=";")
            # loop through line in csv
            for line in reader:
                play_name = line[1]
                if play_name not in self.play_names:
                    continue
                tokens = line[5].split()
                for term in tokens:
                    token = self.clean(term)
                    if token in self.vocab:
                        term_frequency[(play_name, token)] += 1
        return term_frequency

    def cal_cosine(self):
        tf = self.read_csv()
        play_dict = {}
        for play in self.play_names:
            play_vec = []
            for word in self.vocab:
                play_vec.append(tf[(play, word)])
            play_dict[play] = play_vec

        scores = []
        for k1, v1 in play_dict.items():
            for k2, v2 in play_dict.items():
                if k1 <= k2: continue
                scores.append((self.cos_sim(v1, v2), (k1 ,k2)))
        scores.sort(reverse=True)
        print(scores[:25])

    def cos_sim(self, vector1, vector2):
        cosine_similarity = 1 - spatial.distance.cosine(vector1, vector2)
        return cosine_similarity


v = vector_embeddings()
v.load_play_name_list()
v.load_vocab_file()
v.cal_cosine()

