
def factorial(number: int):
    """This is  a factorial of a number using recursion"""

    if number == 0:
        return 1


    #  For large values of number, this may result in a stack overflow.
    
    return factorial(number - 1)  * number



def factorial_optimized(number: int, accumulator=1):
    """
    The main difference is the that the last executable statement is a recursive call to this
    same function.
    """

    if number == 0: 
        return accumulator

  
    # now be passed to the recursive call.
    return factorial_optimized(number-1, accumulator * number)