import argparse
import csv
import os

DEFAULT_INFILE = "players_list_foa.txt"
DEFAULT_OUTFILE = "players_list_foa_converted.csv"

FIELD_NAMES = [
    'ID Number',
    'Name',
    'Fed',
    'Sex',
    'Tit',
    'WTit',
    'OTit',
    'FOA',
    'SRtng',
    'SGm',
    'SK',
    'RRtng',
    'RGm',
    'Rk',
    'BRtng',
    'BGm',
    'BK',
    'B-day',
    'Flag',
]

OUTPUT_COLS = [
    'fideid',
    'name',
    'country',
    'sex',
    'title',
    'o_title',
    'foa_title',
    'rating',
    'k',
    'rapid_rating',
    'blitz_rating',
    'birthday',
    'flag',
]


def find_positions(header, col_names):
    positions = []
    for name in col_names:
        idx = header.find(name)
        positions.append(idx)
    return positions


def slice_fields(line, col_names, positions):
    fields = {}
    for i, name in enumerate(col_names):
        start = positions[i]
        if start == -1:
            fields[name] = ""
            continue
        end = None
        for j in range(i + 1, len(positions)):
            if positions[j] != -1:
                end = positions[j]
                break
        val = line[start:end] if end is not None else line[start:]
        fields[name] = val.strip()
    return fields


def normalize_rating(val):
    val = (val or "").strip()
    if not val or val == '0':
        return ""
    try:
        return f"{float(val):.1f}"
    except ValueError:
        return val


def convert(infile, outfile):
    with open(infile, 'r', encoding='utf-8', errors='replace') as inf, \
         open(outfile, 'w', newline='', encoding='utf-8') as outf:
        header = inf.readline()
        positions = find_positions(header, FIELD_NAMES)

        writer = csv.writer(outf)
        writer.writerow(OUTPUT_COLS)

        for line in inf:
            if not line.strip():
                continue
            fields = slice_fields(line, FIELD_NAMES, positions)

            fideid = fields.get('ID Number', '').split()[0] if fields.get('ID Number') else ''
            name = fields.get('Name', '')
            country = fields.get('Fed', '')
            sex = fields.get('Sex', '')
            title = fields.get('Tit', '')
            o_title = fields.get('OTit') or fields.get('WTit') or ''
            foa_title = fields.get('FOA', '')
            rating = normalize_rating(fields.get('SRtng') or fields.get('MAY26') or fields.get('RDTng') or '')
            k = fields.get('SK') or fields.get('K') or ''
            rapid = normalize_rating(fields.get('RRtng'))
            blitz = normalize_rating(fields.get('BRtng'))
            birthday = fields.get('B-day') or fields.get('BORN') or ''
            flag = fields.get('Flag', '')

            writer.writerow([
                fideid,
                name,
                country,
                sex,
                title,
                o_title,
                foa_title,
                rating,
                k,
                rapid,
                blitz,
                birthday,
                flag,
            ])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert FIDE fixed-width TXT ratings to CSV.')
    parser.add_argument('--input', '-i', default=DEFAULT_INFILE, help='Input TXT file')
    parser.add_argument('--output', '-o', default=DEFAULT_OUTFILE, help='Output CSV file')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Input file not found: {args.input}")
    else:
        print(f"Converting {args.input} -> {args.output} ...")
        convert(args.input, args.output)
        print("Done.")
