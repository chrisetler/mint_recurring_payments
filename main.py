import argparse
import csv
import sys
from _pydecimal import Decimal

FORMAT_STR = "\"Date\",\"Description\",\"Original Description\",\"Amount\",\"Transaction Type\",\"Category\",\"Account Name\",\"Labels\",\"Notes\""


# print an error
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# reads the CSV to a array and returns it
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


# filters the array to just the rows we want (for now just to debits not credits)
def filter_array(data):
    debts_only = list(filter(lambda row: row[4] == 'debit', data))
    return debts_only

# Builds the dict with the data in it
def build_dict(data):
    my_dict = {}
    for row in data:
        key = row[1] + " " + row[2]
        try:
            existing_data = my_dict[key]

            current_count = existing_data["count"]
            current_average = existing_data["average_amount"]
            this_amount = Decimal(row[3])

            new_count = current_count + 1
            new_average = (current_average*current_count + this_amount) / new_count


            existing_data["count"] = new_count
            existing_data["average_amount"] = new_average
            existing_data['earliest_transaction'] = row[0]

        except KeyError as e:
            # no existing data
            value = {}
            count = 1
            this_amount = Decimal(row[3])
            latest_date = row[0] #always assume the newest transactions appear first

            value["latest_transaction"] = latest_date
            value["average_amount"] = this_amount
            value["count"] = count
            my_dict[key] = value


    return my_dict




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", type=str,
                        help="transactions file name. Transactions should be in the file NEWEST TO OLDESTS. File "
                             "should be in format: ")
    parser.add_argument("-d", "--delimiter", type=str, default=",",
                        help="specify the CSV delimiter (default: ,)")
    parser.add_argument("-q", "--quotechar", type=str, default="\"",
                        help="specify the CSV quotechar (default: \")")
    args = parser.parse_args()

    data = read_csv_to_array(args.file_name, args.delimiter, args.quotechar)
    data = filter_array(data)
    print("Filtered length: " + repr(len(data)))

    dict_data = build_dict(data)


