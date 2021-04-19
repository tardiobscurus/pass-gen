l = [[1, 2], [3, 4]]

found = False
p = 2

for i in l:
    for j in i:
        if j == p:
            found = True
            break
        else:
            continue