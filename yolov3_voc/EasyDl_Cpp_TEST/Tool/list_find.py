name =['battary','can','battary','bottle']
name_copy = name.copy()

i= 0
j = i+1
lens = len(name)
while(i < lens):
    while(j < lens):
        if(name[i] == name [j]):
            name.pop(j)
            j -= 1
            lens -= 1
        j+= 1
    i += 1
print(name)
# name_temp = list(set(name))
name_nums = []
for num in range(len(name)):
    name_nums.append(name_copy.count(name[num]))

print(name_nums)
