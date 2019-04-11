import csv
import time

curr_time = time.localtime()

name = str(curr_time.tm_mon) + '_' + str(curr_time.tm_mday) + '_' + str(curr_time.tm_year) + '_griptest' +  '.csv'
print('made it past time')
print(name)

with open(str(name), 'w') as csvfile:
    print('made it past fileopen')
    fwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    print('made it past creating writer')
