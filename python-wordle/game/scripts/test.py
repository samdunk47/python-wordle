import itertools

list = []
for i in range(100):
    list.append(i)
    
for j in itertools.islice(list, 5, 10):
    print(j)