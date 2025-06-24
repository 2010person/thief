import itertools #This is a module in the standard library whicb can iterate to allow for efficiency
num1 = str(int(input())) #taking inputs from the user
num2 = str(int(input()))
num3 = str(int(input()))
num4 = str(int(input()))
nums = "1234"
rearrangement = [" ".join(x) for x in itertools.permutations(nums, 4)] 
for y in rearrangement:
    y 
    for z in list(y):
        pass
ans = []
print(rearrangement)