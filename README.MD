# mint_recurring_payments

## Intro

This script can be used to analyze a recent transactions csv from Mint.com to look for recent transactions.

It outputs a CSV file stream which includes information on repeated transactions it was able to find, including the average number of occurances of that transaction per month, the average amount, the total count, and the earliest and latest date of the transactions

## Usage

```
Python mint_recurring_payments.py transactions.csv > out_file.csv
```

The output file can be opened in Excel or another spreadsheet software for analysis. 
