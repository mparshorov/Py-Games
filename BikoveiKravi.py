import random

def getSecretNum(numDigits):
    numbers=list(range(10))
    random.shuffle(numbers)
    secretNum=''
    for i in xrange(numDigits):
        secretNum+=str(numbers[i])
    return secretNum
def getClues(guess, secretNum):
    if guess==secretNum:
        return 'You got it!'
    clue=[]
    for i in xrange(len(guess)):
        if guess[i]==secretNum[i]:
            clue.append('Bik')
        elif guess[i] in secretNum:
            clue.append('Krava')
    if len(clue) == 0:
        return 'Bagels'
    return ' '.join(clue)
def isNumber(guess):
    if guess=='':
        return False
    for i in guess:
        if int(i) not in [0,1,2,3,4,5,6,7,8,9]:
            return False
    return True
def playAgain():
    return raw_input('Do you want to play again! Y/N\n').upper().startswith('Y')

MAX_DIGITS=3
MAX_TRIES=10

print 'I am thinking of a %d-digit number. Try to guess what it is.' % (MAX_DIGITS)
print 'Here are some clues:' 
print 'When I say:    That means:' 
print '  Krava         One digit is correct but in the wrong position.'
print '  Bik           One digit is correct and in the right position.'
print '  Bagels        No digit is correct.'

while True:
    secretNum=getSecretNum(MAX_DIGITS)
    print "I have thought of a number. You have %d guesses to get it right." % MAX_TRIES
    currentTry=1
    while currentTry<MAX_TRIES:
        guess=''
        while len(guess)!=MAX_DIGITS or not isNumber(guess):
            print 'Guess #%d :' % currentTry
            guess=raw_input()
        clue=getClues(guess, secretNum)
        print clue
        currentTry+=1
        if guess==secretNum:
            break
        if currentTry==MAX_TRIES:
            print 'You ran out of tries. The number was {0}.'.format(secretNum)
    if not playAgain():
        break