import math
import random
import gmpy2 
# Case Van Horsen (2024). Welcome to gmpy2’s documentation! — gmpy2 2.2.1 documentation. [online] Available at: https://gmpy2.readthedocs.io/en/latest/.

# function for converting plaintext to n-bit message
def convertToBinary(m):
    binary = []  # Initialize list to hold all binary digits
    for char in m: binary.extend(int(digit) for digit in bin(ord(char))[2:].zfill(8))
    return binary

# function for converting listing consisting of binary values into plaintext
def convertToString(b):
    return''.join(chr(int(("".join(str(x) for x in b))[i*8:i*8+8],2)) for i in range(len(b)//8)) # every 8 binary values are converted into its string counterpart to form the message

# function used for getting w in gcd(w, q) = 1
def getW(q):
    w = random.randint(0, 2*q) # generates random int between 0 & 2q
    if (math.gcd(w, q)) == 1: return w # base case: returns w checks if the gcd is 1
    else: return getW(q) # recursive case: if gcd is not 1 then try a new w

# function for generating easy key (e)
def generateEasyKey(m):
    e = [] # initialising e as empty list
    for i in range(m): e.append(sum(e) + random.randint(1, int(m/2))) # creating a key with same length as n-bit message and adding numbers which satisfy the conditio
    return e

# function for generating hard key
def generateHardKey(e, q, w):
    return [(w * i) % q for i in e] # creating a key with same length as easy key, following hi = w.ei mod q

# function used for encrypting a message with the hard key
def encrypt(m, h):
    return sum(hi * mi for hi, mi in zip(h, m)) # c = h1m1+ h2m2 + ··· + hnmn

# function used for decripting a ciphertext with the private key
def decrypt(c, e, q, w):
    wPrime = pow(w, -1, q) # w^−1 mod q
    cPrime = c * wPrime % q # c′ = cw^−1 mod q
    mPrime = [] 
    for i in reversed(e): # iterating backwards through easy key
        if cPrime >= i: # checking if key c' is greating than key value
            mPrime.insert(0,1) # mn = 1
            cPrime-=i # compute c′ = c′ − en
        else: mPrime.insert(0,0) # mn = 0
    return convertToString(mPrime)

# reading input from file
def readFile(path):
    try:
        f = open(path, "r")
        message = f.read()
        f.close()
        return message # returning file contents
    except IOError:
        print("Invalid file") # catching error for invalid file

# writing input to file
def writeFile(path, string):
    f = open(path, "w")
    f.write(string) # writing string to file
    f.close()
        
# running functions
fileContents = False
while not(fileContents):
    path = (input("Enter filepath (e.g: input.txt)")).lower()
    if path == "quit": quit()
    fileContents = readFile(path)

# assigning keys and n-bit message    
m = convertToBinary(fileContents)
e = generateEasyKey(len(m))
q = gmpy2.next_prime((2 * e[-1])+1) # used import for getting next prime: https://gmpy2.readthedocs.io/en/latest/ - Case Van Horsen (2024)
w = getW(q)
h = generateHardKey(e,q,w)
# encrypting and decrypting text
ciphertext = encrypt(m, h)
deciphertext = decrypt(ciphertext, e, q, w)

# writing keys, ciphertext, and decrypted text to file
writeFile("e.txt", str(e))
writeFile("q.txt", str(q))
writeFile("w.txt", str(w))
writeFile("h.txt", str(h))
writeFile("ciphertext.txt", str(ciphertext))
writeFile("deciphertext.txt", str(deciphertext))
