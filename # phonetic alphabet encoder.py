# phonetic alphabet encoder
import os
import time

os.system("clear")

print("Welcom to the Encrypter / Phionetic alphabet afier")
print("We now support numbers and words!")
print("")

time.sleep(1)

ut = input("Enter the message you would like to encrypt: ").lower() # Users text they want to "encode" / phonetasise

phonetic = {

    'a': 'Alpha', 'b': 'Bravo', 'c': 'Charlie', 'd': 'Delta',
    'e': 'Echo', 'f': 'Foxtrot', 'g': 'Golf', 'h': 'Hotel',
    'i': 'India', 'j': 'Juliett', 'k': 'Kilo', 'l': 'Lima',
    'm': 'Mike', 'n': 'November', 'o': 'Oscar', 'p': 'Papa',
    'q': 'Quebec', 'r': 'Romeo', 's': 'Sierra', 't': 'Tango',
    'u': 'Uniform', 'v': 'Victor', 'w': 'Whiskey', 'x': 'X-ray',
    'y': 'Yankee', 'z': 'Zulu',
    '1': 'One', '2': 'Two', '3': 'Three', '4': 'Four',
    '5': 'Five', '6': 'Six', '7': 'Seven', '8': 'Eight',
    '9': 'Nine', '0': 'Zero'
}

letter_grid = [list(word) for word in ut.split()]

for word in letter_grid:
    phonetic_word = [phonetic.get(letter, letter) for letter in word] #add .get and .join explinations (claud chat)
    print(' - '.join(phonetic_word))
