from ..constants import LookUpResults
from ..tools import *
from datetime import datetime as dt
import glob
import os
from itertools import zip_longest

def get_uniques(l: list):
    return list(set(l) - set([""]))


def uniq_preserve_order(l: list) -> list:
    return sorted(set(l), key=lambda x: l.index(x))

def truncate_middle(s, n):
    if len(s) <= n:
        return s
    n_2 = int(n / 2 - 3)
    n_1 = int(n - n_2 - 3)
    return '{0}...{1}'.format(s[:n_1], s[-n_2:])

def genPreviewHTML(sentence: str, item: LookUpResults, word_original: str = "") -> str:
    result = f'''<center>{sentence.replace(word_original, f"<b>{word_original}</b>")}</center>
        <hr>
        <center>
            <b>{item.get('word', '')}</b>:
            <br>{item.get('definition', '').strip()}</center>'''
    if item.get('definition2', ''):
        result += f"<hr><center>{item.get('definition2', '')}</center>"
    return result

def date_to_timestamp(datestr: str):
    return dt.strptime(datestr, "%Y-%m-%d %H:%M:%S").timestamp()

def findDBpath(path):
    # KOReader settings may be in a hidden directory
    paths = glob.glob(os.path.join(path, "**/vocabulary_builder.sqlite3"), recursive=True)\
        + glob.glob(os.path.join(path, ".*/**/vocabulary_builder.sqlite3"), recursive=True)
    if paths:
        return paths[0]
    else:
        raise FileNotFoundError("Could not find database in import directory. Please verify that you selected the correct directory.")

def koreader_scandir(path):
    filelist = []
    for filetype in ["epub", "fb2", "fb2.zip", "pdf"]:
        files = glob.glob(os.path.join(path, "**/*." + filetype), recursive=True)
        for filename in files:
            if os.path.exists(os.path.join(os.path.dirname(filename),
                                removesuffix(filename, filetype) + "sdr",
                                "metadata." + filetype + ".lua")):
                filelist.append(filename)
    print(filelist)
    return filelist

def findHistoryPath(path):
    # KOReader settings may be in a hidden directory
    paths = glob.glob(os.path.join(path, "**/lookup_history.lua"), recursive=True)\
        + glob.glob(os.path.join(path, ".*/**/lookup_history.lua"), recursive=True)
    if paths:
        return paths[0]
