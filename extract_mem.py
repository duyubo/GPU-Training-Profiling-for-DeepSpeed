import csv
import os
# open the file in the write modei
s = 0
e = 2
f = open('mem.csv', 'w')
# create the csv writer
writer = csv.writer(f)
for o in [0, 1, 2, 3]:
    writer.writerow(['optimization_level'+str(o), 1, 2, 4, 8, 16, 32, 64, 128])
    for model_name in ["t5-large","t5-3b","t5-11b"]:
        line = []
        line.append(model_name)
        for b in [1, 2, 4, 8, 16, 32, 64, 128]:
            file_name = 'mem_'+str(b)+'_'+str(o)+'_'+model_name+'.log'
            print(file_name)
            exists = os.path.isfile(file_name)
            if exists:
                f = open(file_name)
                lines = f.readlines()
                mem_single = []
                for row in lines:
                    r = row.split('|')
                    value = int(r[2].split('M')[0])
                    mem_single.append(value)
            
                mem_single = [sum(mem_single[i+s:i+e])/(e - s) for i in range(len(mem_single)) if i%8 ==0]
                print(b, o, model_name, max(mem_single))
                line.append(max(mem_single))
            else:
                line.append(9999999)
            
        writer.writerow(line)

for o in [2, 3]:
    writer.writerow(['optimization_level'+str(o), 1, 2, 4, 8, 16, 32, 64, 128])
    for model_name in ["t5-large","t5-3b","t5-11b"]:
        line = []
        line.append(model_name)
        for b in [1, 2, 4, 8, 16, 32, 64, 128]:
            file_name = 'mem_'+str(b)+'_'+str(o)+'_'+model_name+'_offload.log'
            print(file_name)
            exists = os.path.isfile(file_name)
            if exists:
                f = open(file_name)
                lines = f.readlines()
                mem_single = []
                for row in lines:
                    r = row.split('|')
                    value = int(r[2].split('M')[0])
                    mem_single.append(value)
            
                mem_single = [sum(mem_single[i+s:i+e])/(e-s) for i in range(len(mem_single)) if i%8 ==0]
                print(b, o, model_name, max(mem_single))
                line.append(max(mem_single))
            else:
                line.append(9999999)
            
        writer.writerow(line)
# close the file
f.close()
