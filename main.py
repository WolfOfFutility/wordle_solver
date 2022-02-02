import json
import random

## Finds all of the 5 letter words in the English Language 

def find_all_5_letter_words() :
    f = open("all_words.txt", "r")
    w = open("short_list.txt", "a")

    for x in f :
        if len(x) == 6 :
            w.write(x)

    f.close()
    w.close()


## Ranks letters by the amount of times they are used within any of the 5 letter words in the english language

def determine_letter_usage() :
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    alphabet_nums = {
        "a": 0,
        "b": 0,
        "c": 0,
        "d": 0,
        "e": 0,
        "f": 0,
        "g": 0,
        "h": 0,
        "i": 0,
        "j": 0,
        "k": 0,
        "l": 0,
        "m": 0,
        "n": 0,
        "o": 0,
        "p": 0,
        "q": 0,
        "r": 0,
        "s": 0,
        "t": 0,
        "u": 0,
        "v": 0,
        "w": 0,
        "x": 0,
        "y": 0,
        "z": 0
    }

    file = open("short_list.txt", "r")
    for x in file :
        for y in alphabet :
            current_letter_count = x.count(y)
            alphabet_nums[y] += current_letter_count

    num_file = open("num_list.txt", "w")

    num_file.write(json.dumps(alphabet_nums))

    file.close()
    num_file.close()

file = open("num_list.txt", "r")
alpha_nums = json.loads(file.read())
file.close()

sorted_list = dict(sorted(alpha_nums.items(), reverse=True, key=lambda item:item[1]))

popular_letters = []

for x in sorted_list.keys() :
    if len(popular_letters) == 10 :
        break
    else :
        popular_letters.append(x)

## Finds the best words to use for the first word based on letter probability

def find_best_openers() :
    word_file = open("short_list.txt", "r")
    best_first_words = open("first_words.txt", "a")
    for w in word_file :
        first_letter = w.count(popular_letters[0])
        second_letter = w.count(popular_letters[1])
        third_letter = w.count(popular_letters[2])
        fourth_letter = w.count(popular_letters[3])
        fifth_letter = w.count(popular_letters[4])

        if first_letter + second_letter + third_letter + fourth_letter + fifth_letter == 5 :
            if first_letter < 2 and second_letter < 2 and third_letter < 2 and fourth_letter < 2 and fifth_letter < 2 :
                best_first_words.write(w)

    word_file.close()
    best_first_words.close()

## Makes the first guess based on what the best words are

def first_guess() :
    first_words = open("first_words.txt", "r")
    content = first_words.readlines()
    random_num = random.randint(0, len(content) - 1)
    starter_word = content[random_num].strip()

    print("First Guess: " + starter_word)
    first_words.close()

    return starter_word

## Checks the arr for the index of an element. If it isnt in the array, return -1

def check_for_index(arr, element) :
    try :
        index = arr.index(element)
        return index
    except :
        return -1

## Checks if a letter is in a word and returns true or false

def check_letter_in_word(word, letter) :
    if letter in word :
        return True
    else :
        return False

## Loops until it guesses the correct word
# Asks for input each time

def recurrent_guesses(last_word_guessed) :
    last_word = last_word_guessed
    letter_order = ["", "", "", "", ""]
    letters_included = []
    letters_not_included = []
    word_file = open("short_list.txt", "r")
    word_list = word_file.readlines()
    possible_words = []
    try_counter = 1

    l1 = 0
    l2 = 0
    l3 = 0
    l4 = 0
    l5 = 0

    while((l1 + l2 + l3 + l4 + l5) != 10) :
        
        ## Handling Inputs

        l1 = int(input("First Letter Progress: "))
        l2 = int(input("Second Letter Progress: "))
        l3 = int(input("Third Letter Progress: "))
        l4 = int(input("Fourth Letter Progress: "))
        l5 = int(input("Fifth Letter Progress: "))

        letters_arr = [l1, l2, l3, l4, l5]

        ## Turning inputs into letters not included, letters included, and letters in the correct spot

        for x in range(len(letters_arr)) :
            if letters_arr[x] == 1 and last_word[x] not in letters_included :
                letters_included.append(last_word[x])
            elif letters_arr[x] == 2 :
                letter_order[x] = last_word[x]

                if last_word[x] not in letters_included :
                    letters_included.append(last_word[x])

            elif letters_arr[x] == 0 :
                letters_not_included.append(last_word[x])

        ## Check Letters in Different Spot

        if len(letters_included) != 0 : 
            for w in word_list :
                check_arr = []
                word = w.strip()
                
                for l in letters_included :
                    check_arr.append(check_letter_in_word(word, l))
                
                if all(check_arr) and check_for_index(possible_words, word) == -1:
                    possible_words.append(word)
                elif not all(check_arr) and check_for_index(possible_words, word) != -1:
                    possible_words.remove(word)

        ## Check Guaranteed Letters

        if letter_order[0] == "" and letter_order[1] == "" and letter_order[2] == "" and letter_order[3] == "" and letter_order[4] == "" :
            pass
        else :
            if len(possible_words) == 0 :
                possible_words = word_list

            for w in possible_words[:] :
                word = w.strip()
                check_arr = []

                for x in letter_order :
                    if check_for_index(word, x) == check_for_index(letter_order, x) and check_for_index(word, x) != -1 :
                        check_arr.append(True)
                    else :
                        check_arr.append(False)

                if all(check_arr) and check_for_index(possible_words, word) == -1 :
                    possible_words.append(word)
                elif not all(check_arr) and check_for_index(possible_words, word) != -1 :
                    possible_words.remove(word)
                        

        ## Check Letters Not Included

        for w in possible_words[:] :
            word = w.strip()
            check_arr = []

            for m in letters_not_included :
                if check_letter_in_word(word, m):
                    check_arr.append(False)
                else :
                    check_arr.append(True)
            
            if not all(check_arr) and check_for_index(possible_words, word) != -1 :
                possible_words.remove(word)

        last_word = possible_words[random.randint(0, len(possible_words) - 1)]
        print(last_word)    
        try_counter += 1
    
    print("Congratulations, you solved it in " + str(try_counter) + " tries!")
    word_file.close()


## Generates a random word, for testing 

def generate_random_word() :
    five_letter_words = open("short_list.txt", "r")
    list_of_words = five_letter_words.readlines()
    random_num = random.randint(0, len(list_of_words) - 1)
    five_letter_words.close()

    return list_of_words[random_num].strip()


## Starts off the guessing 
start_word = first_guess()
recurrent_guesses(start_word)



    



