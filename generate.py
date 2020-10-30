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

pos_filter = {'NN', 'VVFIN', 'VVINF', 'ADJD', 'ADV'}
min_len = 3
max_len = 10
naughty = ['sex', 'nazi']


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
    os.makedirs(data_dir, exist_ok=True)
    urllib.request.urlretrieve(dereko_url, dereko_zip)


def unpack_dereko():
    with zipfile.ZipFile(dereko_zip, 'r') as zip_ref:
        zip_ref.extractall(data_dir)
    assert dereko_txt.exists()


def parse_dereko() -> List[Token]:
    with dereko_txt.open('r') as fp:
        tokens = [Token.parse_line(line) for line in fp if line]
    return tokens


def get_dereko_tokens() -> List[Token]:
    if not dereko_zip.exists():
        download_dereko()
    if not dereko_txt.exists():
        unpack_dereko()
    tokens = parse_dereko()
    return tokens


def filter_tokens(tokens: List[Token], limit=6**5) -> List[str]:
    # only include tokens that have the specified POS tags
    tokens_pos = [t for t in tokens if t.pos in pos_filter]
    # don't use tokens that are too short or too long
    tokens_len = [t for t in tokens_pos if min_len <= len(t.token) <= max_len]
    # avoid umlauts (äöü) and other non-ascii stuff as well as punctuation
    tokens_no_umlaut = [t for t in tokens_len if t.token.isascii() and t.token.isalpha()]
    # filter out sensitive tokens (there are only few among the most frequent words)
    tokens_not_naughty = [t for t in tokens_no_umlaut if
                          all(x not in t.token.lower() for x in naughty)]
    # sort tokens by frequency and group them by their common normalized form
    tokens_byfreq = sorted(tokens_not_naughty, key=lambda t: t.frequency, reverse=True)
    group_normalized = defaultdict(list)
    for token in tokens_byfreq:
        group_normalized[token.normalized.lower()].append(token)
    # only keep the most frequently used true form of every normalized form
    normalized_first = [tokens[0] for tokens in group_normalized.values()]
    normalized_sorted = sorted(normalized_first, key=lambda t: t.frequency, reverse=True)
    # convert token objects to lower-case plaintext
    plain = list(dict.fromkeys(t.token.lower() for t in normalized_sorted))
    return plain[:limit]


def count_to_dice(n, num_dice=5) -> int:
    digits = []
    while n:
        digits.append((n % 6) + 1)
        n //= 6
    if len(digits) < num_dice:
        digits += [1] * (num_dice - len(digits))
    digite_str = ''.join(str(i) for i in digits[::-1])
    return int(digite_str)


def generate_diceware_txt(tokens: List[str]):
    assert len(tokens) == 6**5
    with diceware_dereko_txt.open('w') as fp:
        for i, token in enumerate(sorted(tokens)):
            dice = count_to_dice(i)
            fp.write(f'{dice}\t{token}\n')


def generate_diceware_json(tokens: List[str]):
    assert len(tokens) == 6**5
    dice_mapping = {count_to_dice(i): token for i, token in enumerate(sorted(tokens))}
    with diceware_dereko_json.open('w') as fp:
        json.dump(dice_mapping, fp, sort_keys=True, ensure_ascii=False, indent=2)


def generate_diceware_js(tokens: List[str]):
    assert len(tokens) == 6**5
    with diceware_dereko_js.open('w') as fp:
        fp.write("var german = {\n")
        dict_lines = [f'  {count_to_dice(i)}: "{token}"' for i, token in enumerate(sorted(tokens))]
        fp.write(',\n'.join(dict_lines))
        fp.write("\n}\n")


def test_selection(tokens: List[str], words=6, repeat=20):
    selection = sorted(tokens[:6 ** 5])
    for i in range(repeat):
        choice = [random.choice(selection) for _ in range(words)]
        print("* " + ", ".join(choice))


def main():
    tokens = get_dereko_tokens()
    filtered = filter_tokens(tokens)
    generate_diceware_txt(filtered)
    generate_diceware_json(filtered)
    generate_diceware_js(filtered)
    test_selection(filtered)


if __name__ == '__main__':
    main()
