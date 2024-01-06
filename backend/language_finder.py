from math import log2
import os
from consts import *
from fcm import FCM


def get_estimated_bits(path, target, k):
    estimated_bits = 0
    symbol_count = k

    fcm = FCM(k)
    fcm.load_index(path)

    with open(target, 'r') as f:
        text = f.read()
        f.close()

    for i in range(len(text) - k):
        ctx = text[i:i+k]
        chr = text[i+k]
        symbol_count += 1

        if fcm.context_exists(ctx):
            if fcm.symbol_exists(ctx, chr):
                estimated_bits += (-log2(fcm.get_symbol_probability(ctx, chr)))
            else:
                estimated_bits += (-log2(SMOOTHING_PARAMETER
                                         / (fcm.get_context_num_ocurrences(ctx)
                                            + (SMOOTHING_PARAMETER * fcm.get_alphabet_size()))))
        else:
            estimated_bits += (-log2(1 / fcm.get_alphabet_size()))

    return estimated_bits / symbol_count


def get_language(target):
    score = {}
    for path in os.listdir(f'cache/k{MAX_CONTEXT_SIZE}/'):
        if path not in score:
            # print(f'Comparing {target} with {path}')
            score[path] = get_estimated_bits(
                f'cache/k{MAX_CONTEXT_SIZE}/{path}', target, MAX_CONTEXT_SIZE)

    return os.path.splitext(min(score, key=score.get))[0]