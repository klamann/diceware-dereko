import json
import os
import random
import urllib.request
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import List, NamedTuple

data_dir = Path('./data')
dereko_url = "http://www1.ids-mannheim.de/fileadmin/kl/derewo/DeReKo-2014-II-MainArchive-STT.100000.freq.zip"
dereko_zip = data_dir / 'dereko-2014.zip'
dereko_txt = data_dir / 'DeReKo-2014-II-MainArchive-STT.100000.freq'
diceware_dereko_txt = data_dir / 'diceware-dereko.txt'
diceware_dereko_json = data_dir / 'diceware-dereko.json'
diceware_dereko_js = data_dir / 'diceware-dereko.js'

pos_filter_base = {'NN', 'VVFIN', 'VVINF', 'ADJD', 'ADV', 'VMFIN', 'VVIMP'}
pos_filter_ext = pos_filter_base | {'NE', 'ADJA', 'APPR', 'PTKVZ', 'PIAT', 'PROAV', 'PPOSAT'}
naughty = ['sex', 'nazi', 'hure']

# note: please adjust these parameters to generate different diceware lists
min_word_len = 3
max_word_len = 10
num_dice = 5


class Token(NamedTuple):
    token: str
    normalized: str
    pos: str
    frequency: float

    @classmethod
    def parse_line(cls, line: str) -> 'Token':
        parts = line.split('\t')
        return Token(token=parts[0], normalized=parts[1], pos=parts[2], frequency=float(parts[3]))


def download_dereko():
    print("downloading DeReKo data")
    os.makedirs(data_dir, exist_ok=True)
    urllib.request.urlretrieve(dereko_url, dereko_zip)


def unpack_dereko():
    with zipfile.ZipFile(dereko_zip, 'r') as zip_ref:
        zip_ref.extractall(data_dir)
    assert dereko_txt.exists()


def parse_dereko() -> List[Token]:
    with dereko_txt.open('r', encoding='utf8') as fp:
        tokens = [Token.parse_line(line) for line in fp if line]
    return tokens


def get_dereko_tokens() -> List[Token]:
    if not dereko_zip.exists():
        download_dereko()
    if not dereko_txt.exists():
        unpack_dereko()
    tokens = parse_dereko()
    return tokens


def filter_tokens(tokens: List[Token], limit=6**5, pos_filter=None, min_len=3, max_len=None,
                  filter_special=False, filter_naughty=True, group_forms=False) -> List[str]:
    # only include tokens that have the specified POS tags
    if pos_filter:
        tokens = [t for t in tokens if t.pos in pos_filter]
    # don't use tokens that are too short or too long
    if min_len or max_len:
        min_len = min_len or 0
        max_len = max_len or 100
        tokens = [t for t in tokens if min_len <= len(t.token) <= max_len]
    # avoid umlauts (äöü) and other non-ascii stuff as well as punctuation
    if filter_special:
        tokens = [t for t in tokens if t.token.isascii() and t.token.isalpha()]
    # filter out sensitive tokens (there are only few among the most frequent words)
    if filter_naughty:
        tokens = [t for t in tokens if all(x not in t.token.lower() for x in naughty)]
    # sort tokens by frequency
    tokens_byfreq = sorted(tokens, key=lambda t: t.frequency, reverse=True)
    # group tokens by their common normalized form
    if group_forms:
        group_normalized = defaultdict(list)
        for token in tokens_byfreq:
            group_normalized[token.normalized.lower()].append(token)
        # only keep the most frequently used true form of every normalized form
        normalized = [tokens[0] for tokens in group_normalized.values()]
        tokens = sorted(normalized, key=lambda t: t.frequency, reverse=True)
    # convert token objects to lower-case plaintext
    tokens = list(dict.fromkeys(t.token.lower() for t in tokens))
    if len(tokens) >= limit:
        return tokens[:limit]
    else:
        raise ValueError(f"Not enough tokens! Got {len(tokens)} after all filters, "
                         f"but required {limit} tokens")


def count_to_dice(n, num_dice=5) -> int:
    digits = []
    while n:
        digits.append((n % 6) + 1)
        n //= 6
    if len(digits) < num_dice:
        digits += [1] * (num_dice - len(digits))
    digite_str = ''.join(str(i) for i in digits[::-1])
    return int(digite_str)


def export_diceware_txt(tokens: List[str], num_dice=5):
    with diceware_dereko_txt.open('w', encoding='utf-8') as fp:
        for i, token in enumerate(sorted(tokens)):
            dice = count_to_dice(i, num_dice)
            fp.write(f'{dice}\t{token}\n')


def export_diceware_json(tokens: List[str], num_dice=5):
    dice_mapping = {count_to_dice(i, num_dice): token
                    for i, token in enumerate(sorted(tokens))}
    with diceware_dereko_json.open('w', encoding='utf-8') as fp:
        json.dump(dice_mapping, fp, sort_keys=True, ensure_ascii=False, indent=2)


def export_diceware_js(tokens: List[str], num_dice=5):
    with diceware_dereko_js.open('w', encoding='utf-8') as fp:
        fp.write("var german = {\n")
        dict_lines = [f'  {count_to_dice(i, num_dice)}: "{token}"'
                      for i, token in enumerate(sorted(tokens))]
        fp.write(',\n'.join(dict_lines))
        fp.write("\n}\n")


def export_diceware(tokens: List[str], num_dice=5):
    if len(tokens) != 6 ** num_dice:
        raise ValueError(f"need exactly 6^{num_dice} ({6 ** num_dice}) tokens")
    export_diceware_txt(tokens, num_dice)
    export_diceware_json(tokens, num_dice)
    export_diceware_js(tokens, num_dice)


def generate_diceware_5():
    tokens = get_dereko_tokens()
    return filter_tokens(
        tokens, limit=6**5, pos_filter=pos_filter_base, min_len=min_word_len,
        max_len=max_word_len, filter_special=True, group_forms=True)


def generate_diceware_6():
    tokens = get_dereko_tokens()
    return filter_tokens(
        tokens, limit=6**6, pos_filter=pos_filter_ext, min_len=min_word_len,
        max_len=13, filter_special=True, group_forms=False)


def print_random(tokens: List[str], words=6, repeat=20):
    for i in range(repeat):
        choice = [random.choice(tokens) for _ in range(words)]
        print("* " + ", ".join(choice))


def main():
    if num_dice == 5:
        tokens = generate_diceware_5()
    elif num_dice == 6:
        tokens = generate_diceware_6()
    else:
        raise ValueError("can only generate diceware lists with 5 or 6 dice")
    export_diceware(tokens, num_dice=num_dice)
    print_random(tokens)


if __name__ == '__main__':
    main()
