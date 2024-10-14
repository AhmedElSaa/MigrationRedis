# -*- coding: utf-8 -*-

#
# Tuto: https://automatetheboringstuff.com/2e/chapter16/
#
# Implement a join operation over to json representation sharing a common
# attribut. See with http://lipn.univ-paris13.fr/~cerin/jointure.pdf
# for algorithms for join operation.
#
import csv
 
def csv_to_json_first_method(csv_file):

    from json import dumps
    #create a dictionary
    data_dict = {}
    my_dict = {}
    with open(csv_file, encoding = 'latin1') as csvfile:
        my_reader = csv.DictReader(csvfile)
        print(my_reader.fieldnames)
        my_data = [my_row for my_row in my_reader]
        for my_row in my_data:
            #print(my_row)
            my_dict = {}
            my_dict[my_reader.fieldnames[0]] = my_row[my_reader.fieldnames[0]]
            my_dict[my_reader.fieldnames[1]] = my_row[my_reader.fieldnames[1]]
            data_dict[my_row[my_reader.fieldnames[2]]] = my_dict
    print("====================")
    my_my_dict = {}
    my_my_dict['test'] = data_dict
    print(my_my_dict)
    #for item in data_dict.items():
    #    print(item)
    #
    # convert both intermediary results to JSON object
    #
    y = dumps(my_my_dict)
    print("====================")
    print(y)
    print(type(y))
    print("====================")

    return y
    
def csv_to_json_second_method(csv_file):

    from json import dumps
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
    # convert intermediary results to JSON object
    #
    z = dumps(data_dict)
    print("====================")
    print(z)
    print(type(z))
    print("====================")

    return z


#
# Compute the join of json1 and json2 according to the data representation
# of json objects given by csv_to_json_first_method()
# Note that json1 and json2 are str, meaning serialized object
# Note also that, the name&surname key is the common an implicit attribute
# for the join.
#
def jointure(json1, json2):

    from json import loads
    from json import dumps

    # First, transform json objects to dictionaries

    d1_name = list(loads(json1))[0]
    #print(d1_name)
    d2_name = list(loads(json2))[0]
    #print(d2_name)

    d1 = loads(json1)[d1_name]
    d2 = loads(json2)[d2_name]

    #print(att_name,type(att_name))
    # Second, iterate through dictionaries
    d_res = {}
    for key1, val1 in d1.items():
        #print(key1, '==', val1)
        for key2, val2 in d2.items():
            #print(key1, '==', key2)
            #print([ord(c) for c in key1],key1,[ord(c) for c in att_name],att_name)
            if key1 == key2:
                d = {}
                d.update(val1)
                d.update(val2)
                #print(d)
                d_res[key1] = d
    my_my_dict = {}
    my_my_dict['test'] = d_res
    z = dumps(my_my_dict)

    return z

# Main program
 
json_one = csv_to_json_first_method("test.csv")
json_two = csv_to_json_first_method("test1.csv")

d = jointure (json_one, json_two)
print(d)