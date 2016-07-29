# Fibonacci generator
def fib(fib):    
    count = 1
    num = 1
    num0 = 0
    num1 = 1
    print str(count) + " " + str(num)
    while count < fib:
        for i in range(fib):
            num = num0 + num1
            num0 = num1
            num1 = num
            count += 1
            print str(count) + " " + str(num)
    print "Count finished"
        
fib(30)