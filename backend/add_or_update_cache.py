from consts import MAX_CONTEXT_SIZE
from fcm import FCM
import os

def add_or_update_cache(new_lang):
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

    # for i in range(MAX_CONTEXT_SIZE):
    # print(f'Computing context size = {MAX_CONTEXT_SIZE}')
    fcm = FCM(MAX_CONTEXT_SIZE)
    if f'{lang_name}.pkl' in os.listdir(f'cache/k{MAX_CONTEXT_SIZE}/'):
        fcm.load_index(f'{lang_name}.pkl')
    fcm.read_file(path)
    fcm.save_index(f'cache/k{MAX_CONTEXT_SIZE}/{lang_name}.pkl')

    print(f'Added {lang_name} to the cache\n')
