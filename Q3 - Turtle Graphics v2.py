from turtle import Turtle
import turtle as trl
import math
# Gather inputs
sides = int(input("Enter the number of sides:"))
length = int(input("Enter the side length:"))
depth = int(input("Enter the recursion depth:"))
# Instantiate turtle
screen = trl.Screen()
t = trl.Turtle()
# Compute data needed to draw in 2 matricies
angle = float(180-(((sides-2)*180)/sides)) # Angle for turns(interior angle of given polygon)
L = float(length/(3**int(depth))) # "non-indentation" length
L2 = (L/2)/math.cos(math.radians(60)) # indentation length
#angle data (0 = 60 degree left, 1 = 120 degree right, 2 = interior angle)
def angle_matrix(s, d): 
    if d == 0:
        return [[2] * s]
    next_matrix = angle_matrix(s, d - 1) 
    new_matrix = []
    for row in next_matrix:
        new_row = []
        for item in row:
            new_row.extend([0, 1, 0, item]) # 
        new_matrix.append(new_row)
    return new_matrix
#length data (0 = L, 1 = L2)
def length_matrix(s, d):    #()
    if d == 0:
        return [[1]*4]
    new_matrix = []
    new_row = []
    new_row.extend([1, 0, 0, 1]*4**int(d))
    new_matrix.append(new_row)
    return new_matrix
# Draw from matrix data
size=len(angle_matrix(sides, depth)[0])

for k in range(0,size):
    a = angle_matrix(sides, depth)[0][k]
    l = length_matrix(sides, depth)[0][k]
    if l==0:
        t.forward(L)
    elif l==1:
        t.forward(L2)
    if a==0:
        t.left(60)
    elif a==1:
        t.right(120)
    elif a==2:
        t.left(angle)
    
t.hideturtle()
trl.done()
