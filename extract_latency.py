import csv
import os
# open the file in the write mode
f = open('latency.csv', 'w')
# create the csv writer
writer = csv.writer(f)
for o in [0, 1, 2, 3]:
    writer.writerow(['optimization_level'+str(o), 1, 2, 4, 8, 16, 32, 64, 128])
    for model_name in ["t5-large","t5-3b","t5-11b"]:
        line = []
        line.append(model_name)
        for b in [1, 2, 4, 8, 16, 32, 64, 128]:
            file_name = str(b)+'_'+str(o)+'_'+model_name+'.txt'
            print(file_name)
            exists = os.path.isfile(file_name)
            if not exists:
                line.append(-9999)
                continue
            f = open(file_name)
            lines = f.readlines()
            adder = 0
            iter_list = []
            for row in lines:
                word = "forward_microstep:"
                if word in row:
                    r = row.split('|')
                    rs = sum([float(r[i].split(':')[1]) for i in [1,2,5]])
                    iter_list.append(rs)
            
            if len(iter_list) <= 2:
                print(b, o, model_name, '--')
                line.append('--')
            else:
                index_end = len(iter_list)
                if b <= 16:
                    index_end = index_end//b
                adder = (sum(iter_list[2:index_end])/(index_end - 2))*index_end
                adder /= 1000
                if b > 16:
                    adder /= (b/32)
                print(b, o, model_name, adder)
                line.append(adder)
        writer.writerow(line)


for o in [2, 3]:
    writer.writerow(['optimization_level'+str(o), 1, 2, 4, 8, 16, 32, 64, 128])
    for model_name in ["t5-large","t5-3b","t5-11b"]:
        line = []
        line.append(model_name)
        for b in [1, 2, 4, 8, 16, 32, 64, 128]:
            file_name = str(b)+'_'+str(o)+'_'+model_name+'_offload.txt'
            print(file_name)
            exists = os.path.isfile(file_name)
            if not exists:
                line.append(-9999)
                continue
            f = open(file_name)
            lines = f.readlines()
            adder = 0
            iter_list = []
            for row in lines:
                word = "forward_microstep:"
                if word in row:
                    r = row.split('|')
                    rs = sum([float(r[i].split(':')[1]) for i in [1, 2, 5]])
                    iter_list.append(rs)
            
            if len(iter_list) <= 2:
                print(b, o, model_name, '--')
                line.append('--')
            else:
                index_end = len(iter_list)
                if b <= 16:
                    index_end = index_end//b
                adder = (sum(iter_list[2:index_end])/(index_end - 2))*index_end
                adder /= 1000
                if b > 16:
                    adder /= (b/32)
                print(b, o, model_name, adder)
                line.append(adder)
        writer.writerow(line)


# close the file
f.close()
