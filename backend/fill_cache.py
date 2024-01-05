import os
from consts import MAX_CONTEXT_SIZE

if __name__ == '__main__':
    os.system('mkdir cache')
    for i in range(MAX_CONTEXT_SIZE):
        os.system(f'mkdir -p cache/k{i+1}')
    for path in os.listdir('./langs/'):
        os.system(f'python3 add_new_lang_to_cache.py -f {path}')
