import argparse
import csv
import sys

FORMAT_STR = "\"Date\",\"Description\",\"Original Description\",\"Amount\",\"Transaction Type\",\"Category\",\"Account Name\",\"Labels\",\"Notes\""

# print an error
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def read_csv_to_array(filename, delimiter, quotechar):
    try:
        with open(filename, 'rt') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
            data = []
            for row in csvreader:
                data.append(row)

            print("Done reading CSV")
            print("lines: " + repr(len(data)))
            return data
    except:
        eprint("Failed to parse CSV file")
        eprint("Make sure file exists and is in format: " + FORMAT_STR)
        sys.exit(1)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", type=str,
                        help="transactions file name. File should be in format: ")
    parser.add_argument("-d", "--delimiter", type=str, default=",",
                        help="specify the CSV delimiter (default: ,)")
    parser.add_argument("-q", "--quotechar", type=str, default="|",
                        help="specify the CSV quotechar (default: |)")
    args = parser.parse_args()


    data = read_csv_to_array(args.file_name,args.delimiter,args.quotechar)
