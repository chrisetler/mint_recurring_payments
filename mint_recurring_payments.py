import argparse
import csv
import sys
from _pydecimal import Decimal

FORMAT_STR = "\"Date\",\"Description\",\"Original Description\",\"Amount\",\"Transaction Type\",\"Category\",\"Account Name\",\"Labels\",\"Notes\""

IS_VERBOSE = False


# print an error
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def vprint(*args, **kwargs):
    if(IS_VERBOSE):
        print(*args, **kwargs)


# reads the CSV to a array and returns it
def read_csv_to_array(filename, delimiter, quotechar):
    try:
        with open(filename, 'rt') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
            data = []
            for row in csvreader:
                data.append(row)

            vprint("Done reading CSV")
            vprint("lines: " + repr(len(data)))
            return data
    except:
        vprint("Failed to parse CSV file")
        vprint("Make sure file exists and is in format: " + FORMAT_STR)
        sys.exit(1)


# filters the array to just the rows we want (for now just to debits not credits)
def filter_array(data):
    debts_only = list(filter(lambda row: row[4] == 'debit', data))
    return debts_only

# Builds the dict with the data in it
def build_dict(data):
    my_dict = {}
    for row in data:
        # key = row[1] + " " + row[2]
        key = row[1]
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



    # remove ones where count is only one
    my_dict = dict(filter(lambda x: x[1]["count"] > 1, my_dict.items()))
    return my_dict


def compute_times_per_month_for_dict(my_dict):
    for key, value in my_dict.items():
        start_date = value["earliest_transaction"]
        end_date = value["latest_transaction"]

        start_year = int(start_date.split("/")[2])
        end_year = int(end_date.split("/")[2])

        start_month = int(start_date.split("/")[0])
        end_month = int(end_date.split("/")[0])

        month_diff= (end_month + 12*end_year) - (start_month + 12*start_year)

        if(month_diff==0):
            my_dict[key]["transactions_per_month"] = "NA"

        else:
            transactions_per_month = value["count"] / month_diff
            my_dict[key]["transactions_per_month"] = transactions_per_month


    # filter out NA
    my_dict = dict(filter(lambda x: x[1]["transactions_per_month"] is not "NA", my_dict.items()))
    return my_dict



def print_dict(my_dict):
    print("Name,Transactions Per Month, Average Amount, Count, Earliest Transaction, Latest Transaction")
    for row in my_dict:
        key = row[0]
        value = row[1]

        avg = value["average_amount"]
        avg = "{:0.2f}".format(avg)

        print(key + "," + repr(value["transactions_per_month"]) + "," + avg + "," + repr(value["count"]) + "," + value["earliest_transaction"] + "," +value["latest_transaction"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", type=str,
                        help="transactions file name. Transactions should be in the file NEWEST TO OLDESTS. File "
                             "should be in format: ")
    parser.add_argument("-d", "--delimiter", type=str, default=",",
                        help="specify the CSV delimiter (default: ,)")
    parser.add_argument("-q", "--quotechar", type=str, default="\"",
                        help="specify the CSV quotechar (default: \")")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="show verbose messages")
    args = parser.parse_args()

    if(args.verbose):
        IS_VERBOSE=True

    data = read_csv_to_array(args.file_name, args.delimiter, args.quotechar)
    data = filter_array(data)
    vprint("Filtered length: " + repr(len(data)))

    dict_data = build_dict(data)
    vprint("Pre filtered length: " + repr(len(dict_data.items())))

    dict_data = compute_times_per_month_for_dict(dict_data)

    vprint("Final length: " + repr(len(dict_data.items())))

    # sort by value
    dict_data = sorted(dict_data.items(), key=lambda kv: abs(1-kv[1]["transactions_per_month"]))
    print_dict(dict_data)





