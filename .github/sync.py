import json
import csv
import sys
import os

FIELDS = ['id', 'name', 'logo', 'address', 'purpose']


def read_csv(path='data.csv'):
    with open(path, 'r', encoding='utf-8') as f:
        return [row for row in csv.DictReader(f)]


def write_json(rows, path='data.json'):
    data = []
    for row in rows:
        entry = {}
        for field in FIELDS:
            value = row.get(field, '')
            entry[field] = value.strip() if isinstance(value, str) else value
        data.append(entry)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')


def main():
    if not os.path.exists('data.csv'):
        print('data.csv not found; skipping sync.')
        return
    rows = read_csv()
    if not rows:
        print('data.csv is empty; nothing to sync.')
        return
    write_json(rows)
    print('Regenerated data.json from data.csv ({0} rows).'.format(len(rows)))


if __name__ == '__main__':
    sys.exit(main())