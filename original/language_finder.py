from math import log2
import sys
import argparse
import os
from consts import SMOOTHING_PARAMETER
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Find language of target file')
    parser.add_argument('-t', '--target', required=True, type=str)
    parser.add_argument('-s', '--size', required=True, type=int)
    args = parser.parse_args(sys.argv[1::])

    k = args.size
    target = args.target

    score = {}
    for path in os.listdir(f'cache/k{k}/'):
        if path not in score:
            score[path] = get_estimated_bits(
                f'cache/k{k}/{path}', target, k)
            print(
                f'{os.path.splitext(path)[0]} -> {round(score[path], 3)} bits')

    if len(target.split('/')) > 1:
        target = target.split('/')[-1]
    print(
        f'The text {target} is most likely written in {os.path.splitext(min(score, key=score.get))[0]}')
