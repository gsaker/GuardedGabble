list = [1,2,6,3,9,6,4,2]
swapMade = True
while swapMade:
    swapMade = False
    for i in range (len(list)-1):
        if list[i+1] < list [i]:
            temp = list [i]
            list[i] = list[i+1]
            list[i+1] = temp
            swapMade = True
print(list)