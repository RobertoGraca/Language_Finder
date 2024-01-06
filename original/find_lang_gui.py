from math import log2
import sys
import argparse
import os
from consts import SMOOTHING_PARAMETER
from fcm import FCM
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

target_path = ''
k_value = 0
k_list = None
main_label = None


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


def get_file_language():
    global target_path, k_value, main_label

    if target_path == '' or k_value == 0:
        main_label.configure(
            text='You need to choose a file and a Context Size')
        return

    main_label.configure(
        text='Looking through the caches')

    score = {}
    for path in os.listdir(f'cache/k{k_value}/'):
        if path not in score:
            score[path] = get_estimated_bits(
                f'cache/k{k_value}/{path}', target_path, k_value)
            print(
                f'{os.path.splitext(path)[0]} -> {round(score[path], 3)} bits')

    name = target_path.split('/')[-1]
    main_label.configure(
        text=f'The text {name} is most likely written in {os.path.splitext(min(score, key=score.get))[0]}')


def browse_files():
    global target_path, main_label, k_value
    target_path = filedialog.askopenfilename(initialdir="./examples",
                                             title="Select a File",
                                             filetypes=(("Text files",
                                                         "*.txt*"),
                                                        ("all files",
                                                         "*.*")))
    main_label.configure(text=f'File: {target_path}\nContext Size: {k_value}')


def select_context_size(*args):
    global k_value, k_list, target_path, main_label
    idxs = k_list.curselection()
    if len(idxs) == 1:
        k_value = idxs[0]+1

        main_label.configure(
            text=f'File: {target_path}\nContext Size: {k_value}')


if __name__ == '__main__':
    root = Tk()
    root.title("Language Finder")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    target = StringVar()
    k = StringVar()

    main_label = tk.Label(root, text="Choose a file and a Context Size",
                          width=50, height=4,
                          fg="blue")
    button_browse = ttk.Button(
        root, text='Browse Files', command=browse_files)
    k_list = Listbox(root, listvariable=StringVar(value=list(range(1, 11))))
    button_language = ttk.Button(
        root, text='Determine Language', command=get_file_language)

    main_label.grid(column=1, row=0)
    button_browse.grid(column=0, row=1, sticky=E)
    k_list.grid(column=1, row=1, rowspan=3, sticky=(N, S, E, W))
    button_language.grid(column=2, row=1, sticky=E)

    k_list.bind('<Double-1>', select_context_size)
    root.bind('<Return>', get_file_language)

    root.mainloop()

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(prog='find_lang.py',description='Determine the language of a file')
#     parser.add_argument('-t','--target', required=True, type=str)
#     parser.add_argument('-k', '--size', required=True, type=int, choices=range(1,11))
#     args = parser.parse_args(sys.argv[1::])

#     target = args.target
#     context_size = args.size

#     score = {}

#     for path in os.listdir(f'cache/k{context_size}/'):
#         if path not in score:
#             score[path] = get_estimated_bits(f'cache/k{context_size}/{path}', target, context_size)
#             print(f'{os.path.splitext(path)[0]} -> {round(score[path], 3)} bits')

#     print(f'The text is most likely written in {os.path.splitext(min(score, key=score.get))[0]}')
