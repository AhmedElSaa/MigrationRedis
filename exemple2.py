#
# Tuto: https://automatetheboringstuff.com/2e/chapter16/
#
import csv
from json import dumps
 
def csv_to_json(csv_file):

    #create a dictionary
    data_dict = {}
    my_dict = {}
    with open(csv_file, encoding = 'latin1') as csvfile:
        my_reader = csv.DictReader(csvfile)
        my_data = [my_row for my_row in my_reader]
        for my_row in my_data:
            #print(my_row)
            my_dict = {}
            my_dict['Test 1'] = my_row['Test 1']
            my_dict['Test 2'] = my_row['Test 2']
            data_dict[my_row['Prénom et nom']] = my_dict
    print("====================")
    my_my_dict = {}
    my_my_dict['test'] = data_dict
    print(my_my_dict)
    #for item in data_dict.items():
    #    print(item)
    
    #create a dictionary
    data_dict = {}
    csv_rows = []
    #open a csv file handlerh
    with open(csv_file, encoding = 'latin1', newline='') as csv_file_handler:
        csv_reader = csv.DictReader(csv_file_handler)
        field = csv_reader.fieldnames
        for row in csv_reader:
            #print([{field[i]:row[field[i]] for i in range(len(field))}])
            csv_rows.extend([{field[i]:row[field[i]] for i in range(len(field))}])

    print("====================")
    data_dict['test'] = csv_rows
    #print(type(csv_rows))
    print(data_dict)
    #print(data_dict['test'][0])
    #print("====================")

    #
    # convert both intermediary results to JSON object
    #
    y = dumps(my_my_dict)
    z = dumps(data_dict)
    print("====================")
    print(y)
    print(type(y))
    print("====================")
    print(z)
    print(type(z))

#Step 1
 
csv_to_json("test.csv")