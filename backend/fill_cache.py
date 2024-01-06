import os
from consts import MAX_CONTEXT_SIZE
from add_or_update_cache import *

if __name__ == '__main__':
    os.system('mkdir cache')
    #for i in range(MAX_CONTEXT_SIZE):
    os.system(f'mkdir -p cache/k{MAX_CONTEXT_SIZE}')
    for path in os.listdir('./langs/'):
        add_or_update_cache(path)
