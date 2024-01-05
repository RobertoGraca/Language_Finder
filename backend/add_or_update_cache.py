from consts import MAX_CONTEXT_SIZE
import fcm
from fcm import FCM
import argparse
import sys
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Add dataset for new languages')
    parser.add_argument('-f', '--file', required=True, type=str)
    args = parser.parse_args(sys.argv[1::])

    new_lang = args.file

    path = ''

    if new_lang not in os.listdir('.'):
        if new_lang not in os.listdir('langs/'):
            print('File could not be located!')
            exit(2)
        else:
            path = 'langs/'

    path += new_lang

    lang_name = os.path.splitext(new_lang)[0]

    print(f'Creating dataset for {lang_name}')

    for i in range(MAX_CONTEXT_SIZE):
        print(f'Computing context size = {i+1}')
        fcm = FCM(i+1)
        if f'{lang_name}.pkl' in os.listdir(f'cache/k{i+1}/'):
            fcm.load_index(f'{lang_name}.pkl')
        fcm.read_file(path)
        fcm.save_index(f'cache/k{i+1}/{lang_name}.pkl')

    print(f'Added {lang_name} to the cache\n')
