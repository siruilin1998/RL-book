class Die():
    def __init__(self, sides):
        self.sides = sides

    def __repr__(self):
       return f"Die(sides = {self.sides})"
       #return "Die(sides = {})".format(self.sides + 1)

    def __eq__(self, other): #Override __eq__
        return self.sides == other.sides

    def __add__(self, other): #Override __add__
        return Die(self.sides + other.sides)

print(Die(6))
print(isinstance(Die(6), Die)) #True
print(Die(10) + Die(11))
print(Die(6) == Die(6))
