import itertools #This is a module in the standard library whicb can iterate to allow for efficiency
try: 
    #taking inputs from the user
    num1 = str(int(input()))
    num2 = str(int(input()))
    num3 = str(int(input()))
    num4 = str(int(input()))
    nums = "1234"
    rearrangement = [" ".join(x) for x in itertools.permutations(nums, 4)] 
    for y in rearrangement:
        y = 
        for z in list(y):
            pass
    ans = []
    print(rearrangement)
except ValueError:
    print("Ooops, it would seem like you haven't inputted a number, please try again!")