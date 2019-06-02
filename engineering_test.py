import os
import subprocess
import re
import collections
import csv

states = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

directory = 'C:\\Users\\L\\PycharmProjects\\untitled\\engineering_test'


def get_filenames(directory):
    filenames = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith('.pdf'):
            filenames.append(filename)
    return filenames

def get_state_indices(alist):
    num_list = []
    state_names = list(states.keys())
    for state in state_names:
        if state.upper() in alist:
            num_list = [i for i, s in enumerate(alist) if state.upper() in s]
    return num_list

def partition(alist, index_list): #splits list into sublists
    sublists = [alist[i:j] for i, j in zip([0] + index_list, index_list + [None])]
    return sublists[1:]

def clean_list(sublist): #deletes unneeded list entries
    rate_indices = [i for i, s in enumerate(sublist) if 'Rate' in s]
    age_indices = [i for i, s in enumerate(sublist) if s == 'Age']
    del_list = rate_indices + age_indices
    for index in sorted(del_list, reverse=True):
        del sublist[index]
    return sublist[:-1]

def format_list(sublist): #formats list to match csv headers
    sublist.insert(0, "x")
    sublist.insert(2, "y")
    d = dict(zip(sublist[::2], sublist[1::2]))
    od = collections.OrderedDict(sorted(d.items()))
    final_list = list(dict.values(od))
    final_list.insert(0, final_list.pop(-3))
    final_list.insert(0, final_list.pop(-2))
    final_list.insert(0, final_list.pop(-2))
    final_list.insert(4, final_list[3]) #adds 0-18 data
    final_list.insert(49, final_list[48]) #adds 65+ data
    final_list[2] = final_list[2][:6]
    final_list[0] = final_list[0][11:]
    state_name = final_list[1]
    n = '%s%s' % (state_name[0].upper(), state_name[1:].lower())
    final_list[1] = states.get(n)
    return final_list

def find_date(string): #finds dates formatted xx/xx/xxxx
    date_regex = re.compile(r'\d{2}/\d{2}/\d{4}')
    date = date_regex.findall(string)
    return date

def format_date(date):
    new_date = date.replace('/', '-')
    new_date = new_date[6:] + '-' + new_date[:5] + ' 00:00:00 UTC'
    return new_date

def write_to_csv(result):
    with open('BeneFix Small Group Plans upload template.csv', 'a', newline='') as result_file:
        wr = csv.writer(result_file, dialect='excel')
        wr.writerow(result)

def main(directory): #NOTE: output omits last column for certain pages of the pdfs. No data from those pages is included in the final csv.
    for file in get_filenames(directory):
        args = ["pdftotext",
                file,
                '-']
        res = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = res.stdout.decode('utf-8').split('\r')
        newlines_removed = [x.strip() for x in output]
        blanks_removed = [x for x in newlines_removed if x]
        indices = get_state_indices(blanks_removed)
        sublists = partition(blanks_removed, indices)
        for s in sublists:
            if len(s) == 104:
                a = clean_list(s)
                final_list = format_list(a)
                dates = find_date(final_list[-1])
                start = format_date(dates[0])
                end = format_date(dates[1])
                final_list.insert(0, start)
                final_list.insert(1, end)
                print(final_list)
                write_to_csv(final_list[:-1])

main(directory)