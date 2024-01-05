import pickle
from consts import MAX_CONTEXT_SIZE, SMOOTHING_PARAMETER


class FCM:
    def __init__(self, context_size):
        assert(context_size > 0 and context_size <= MAX_CONTEXT_SIZE)
        self.k = context_size
        self.alpha = SMOOTHING_PARAMETER
        self.alphabet = set()
        self.index = {}
        self.ctx_count = {}

    def read_file(self, path):
        with open(path, 'r') as f:
            text = f.read()
            self.alphabet.update(set(text))
            f.close()

        for i in range(len(text) - self.k):
            ctx = text[i:i+self.k]
            chr = text[i+self.k]
            self.update_index(ctx, chr)

    def update_index(self, context, symbol):
        assert len(context) == self.k
        assert len(symbol) == 1

        if context not in self.index:
            self.index[context] = {}

        if context not in self.ctx_count:
            self.ctx_count[context] = 0

        if symbol not in self.index[context]:
            self.index[context][symbol] = 0

        self.index[context][symbol] += 1
        self.ctx_count[context] += 1

    def get_alphabet_size(self):
        return len(self.alphabet)

    def get_context_num_ocurrences(self, context):
        assert len(context) == self.k
        return self.ctx_count[context]

    def get_symbol_num_ocurrences(self, context, symbol):
        assert len(context) == self.k
        assert len(symbol) == 1
        return self.index[context][symbol]

    def context_exists(self, context):
        assert len(context) == self.k
        return context in self.index

    def symbol_exists(self, context, symbol):
        assert len(context) == self.k
        assert len(symbol) == 1
        return symbol in self.index[context]

    def get_symbol_probability(self, context, symbol):
        return (self.index[context][symbol] + self.alpha) \
            / (self.ctx_count[context] + (len(self.alphabet) * self.alpha))

    def save_index(self, path):
        assert path.endswith('.pkl')

        with open(path, 'wb') as f:
            pickle.dump([self.index, self.ctx_count, self.alphabet], f)
            f.close()

        print(f'Saved index to {path}')

    def load_index(self, path):
        assert path.endswith('.pkl')

        with open(path, 'rb') as f:
            self.index, self.ctx_count, self.alphabet = pickle.load(f)
            f.close()

        print(f'Loaded index from {path}')
