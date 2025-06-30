import itertools #This is a module in the standard library whicb can iterate to allow for efficiency
from Flask import Flask, render_template, request #Flask allows me to create a backend for the website
app = Flask(__name__) 

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/thief", methods=["POST", "GET"])
def thief():
    if request.method == "POST":
        try: 
            #taking inputs from the user
            num1 = str(int(request.form.get("num1", "")))
            num2 = str(int(request.form.get("num2", "")))
            num3 = str(int(request.form.get("num3", "")))
            num4 = str(int(request.form.get("num4", "")))
            nums = num1 + num2 + num3 + num4
            rearrangement = [" ".join(x) for x in itertools.permutations(nums, 4)] 
            ans = []
            for y in rearrangement:
                ans.append(y)
            ans = list(set(ans)) # This ensure that I can remove duplicated ones
            print(ans)
            return render_template('thief.html', ans=ans, num1=num1, num2=num2, num3=num3, num4=num4)
        except ValueError:
            print("Ooops, it would seem like you haven't inputted a number, please try again!")