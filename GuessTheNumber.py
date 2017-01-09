'''
This is a Guess the Number Game
'''
from random import randint
name=raw_input("Hello! What's your name?\n")
print "Well, {0}, I am thinking of a number between 1 and 20.".format(name)
actNum=randint(1,20)
number=0
for i in xrange(6):
    number=input("Take a guess.\n")
    if number > actNum:
        print "Your guess is too high."
        continue
    elif number < actNum:
        print "Your guess is too low."
        continue
    elif number == actNum:
        print "Good job, {0}! You guessed my number in {1} guesses!"\
        .format(name,i+1)
        break
if number!=actNum:
    print "Nope. The number I was thinking of was {0}".format(actNum)