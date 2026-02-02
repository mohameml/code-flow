import sys

def trace(frame, event, arg):
    if event == "line":
        print(frame.f_locals)
    if event == "return" : 
        print(f"Return is : {arg}")
    return trace 
sys.settrace(trace)

def f(n):
    x = n + 1
    return x

f(2)
