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

    def term_context(self):
        term_context = defaultdict(lambda: defaultdict(lambda: 0))
        with open("ShakespearePlays_text.csv", "r") as f:
            # load csv
            reader = csv.reader(f, delimiter=";")
            # loop through line in csv
            for line in reader:
                play_name = line[1]
                if play_name not in self.play_names:
                    continue
                tokens = line[5].split()
                sentence = []
                for term in tokens:
                    token = self.clean(term)
                    sentence.append(token)
                for i in range(len(sentence)):
                    word = sentence[i]
                    for j in range(max(0, i - 4), min(len(sentence), i + 5)):
                        term_context[word][sentence[j]] += 1
        return term_context

    def compute_word_similarity(self, words):
        tc = self.term_context()
        print(len(tc))

        def to_vec(w):
            vec = []
            for x in self.vocab:
                vec.append(tc[w][x])
            return vec

        for word in words:
            word_vec = to_vec(word)
            scores = []
            c = 0
            for k in tc.keys():
                if k == word: continue
                k_vec = to_vec(k)
                scores.append((self.cos_sim(word_vec, k_vec), k))
                c += 1
                # if  c > 10: break
            scores.sort(reverse=True)
            print("Top-5 matches for " + word + ": ", scores[:5])

    def cos_sim(self, vector1, vector2):
        cosine_similarity = 1 - spatial.distance.cosine(vector1, vector2)
        return cosine_similarity


v = vector_embeddings()
v.load_play_name_list()
v.load_vocab_file()
v.compute_word_similarity([
    "romeo",
    "juliet",
    "nobleman",
    "caesar",
    "friend"
])
