import argparse
import csv

"""
This script switches the order of two columns in a CSV file.
Usage: python change_column_order.py --filename <path to CSV file> --c1 <name of first column> --c2 <name of second column>
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', help='Path to the CSV file')
    parser.add_argument('--c1', required=True, help='Name of first column to switch')
    parser.add_argument('--c2', required=True, help='Name of second column to switch')
    args = parser.parse_args()

    # Read the CSV file and switch the specified columns
    with open(args.filename) as f:
        reader = csv.reader(f)
        headers = next(reader)
        headers = headers[0].split(';')
        if args.c1 not in headers or args.c2 not in headers:
            print(f'Error: One of the specified columns was not found in the header: {headers}')
            return
        c1_index = headers.index(args.c1)
        c2_index = headers.index(args.c2)
        headers[c1_index], headers[c2_index] = headers[c2_index], headers[c1_index]

        rows = [row for row in reader]

    # Write the modified data to a new CSV file
    with open(f'{args.filename.rsplit(".", 1)[0]}_modified.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

if __name__ == '__main__':
    main()
