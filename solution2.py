import csv, sys, pycountry, datetime
from collections import defaultdict, Counter
data = []

def inWhichCountryIsRegion(check_region):
    for region in list(pycountry.subdivisions):
        if region.name == check_region:
            return pycountry.countries.get(alpha_2=region.country_code).alpha_3

def evalPercentString(percent_string):
    return eval(percent_string[0:-1])/100

def howManyClicks(impression, CTR):
    CTR_number = evalPercentString(CTR)
    return round(impression*CTR_number)

def changeDateFormat(date):
    return datetime.datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')

def read_data():
    with open('input.csv', 'r', encoding='utf8', newline='') as csv_file: #can be UTF-8 or UTF-16, new line can be either Unix or ???
        csv_reader = csv.reader(csv_file)
        try:
            for row in csv_reader:
                data.append(row) 
                    
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format("idontunderstand", csv_reader.line_num, e)) #to be done

def transform_data(data):
    for instance in data:

        instance[0]= changeDateFormat(instance[0]) 
        instance[1]= inWhichCountryIsRegion(instance[1])
        if instance[1] == None: #setting unknow country to unknow region
            instance[1]= "XXX"
        instance[2]= eval(instance[2])
        instance[3]= howManyClicks(instance[2],instance[3])
    return sorted(data, key = lambda x: (x[0],x[1]))

    

def reduce_duplication(data):
    counter = Counter()
    counter2 = Counter()

    for date, country_code, impression, CTI in data:
        counter[(date, country_code)] += impression
        counter2[(date,country_code)] += CTI

    outputdata = [[date, country_code, impression] for (date,country_code), impression in counter.items()]

    extra_data = [[date, country_code, CTI] for (date, country_code), CTI in counter2.items()]

    for i in range(len(outputdata)):
        outputdata[i].append(extra_data[i][2])
    return outputdata

def write_to_csv():
    with open('output.csv', mode='w') as writer:
        writer = csv.writer(writer, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in outputdata:
            writer.writerow(row)



read_data()
new_data = transform_data(data)
outputdata = reduce_duplication(new_data)
write_to_csv()

#TO DO error handling, make code prettier and more readable
#sys.stderr.write("An error has occured!") or sys.exit("Error!")
