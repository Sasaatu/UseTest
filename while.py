
print("Please lise the purchase price.")
sum : int = 0
n : int  = 0

while(1):
    try:  # try codes
        price = int(input())
        sum += price
        n += 1

    except EOFError: # when exeption occurs
        break

    
print("you ate %d times and total cost is %d." %(n, sum))
