import json
import csv
import subprocess
import sys
import os

FIELDS = ['id', 'name', 'logo', 'address', 'purpose']


def read_json(path='data.json'):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def read_csv(path='data.csv'):
    with open(path, 'r', encoding='utf-8') as f:
        return [row for row in csv.DictReader(f)]


def write_json(rows, path='data.json'):
    data = []
    for row in rows:
        entry = {}
        for field in FIELDS:
            entry[field] = row.get(field, '').strip() if isinstance(row.get(field), str) else row.get(field, '')
        data.append(entry)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')


def write_csv(rows, path='data.csv'):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, '') for field in FIELDS})


def changed_files():
    try:
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD', '--', 'data.json', 'data.csv'],
            capture_output=True, text=True, check=False,
        ).stdout.strip().split()
    except Exception:
        result = []
    return set(result)


def main():
    if not os.path.exists('data.csv'):
        return
    changed = changed_files()
    if 'data.csv' in changed:
        print('data.csv changed: regenerating data.json from CSV')
        write_json(read_csv())
    elif 'data.json' in changed:
        print('data.json changed: regenerating data.csv from JSON')
        write_csv(read_json())
    else:
        print('No data file change detected; nothing to sync.')


if __name__ == '__main__':
    sys.exit(main())