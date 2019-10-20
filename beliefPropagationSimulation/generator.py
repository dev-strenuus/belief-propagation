import random
sum = 0
v = [0]*8
for i in range(8):
    v[i] = random.randint(1,100)
    sum = sum + v[i]
for i in range(8):
    v[i] = v[i] / sum
    print(v[i])