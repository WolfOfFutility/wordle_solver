# from cgi import test
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

## Searches for the not positions of the included letters, and includes another position if it exists
def check_and_add_non_position(arr, position, letter) :
    existing = False

    ### *** CURRENTLY NOT FILTERING LETTERS CORRECTLY *** 
    try :
        for a in arr :
            if a['letter'] == letter and a['non_pos'].count(position) <= 0 :
                a['non_pos'].append(position)
                existing = True
                break
        
    except :
        print("Error Searching Non Position.")

    return existing

## Checks if a letter is in a position it isnt supposed to be
def check_letter_not_in_position(arr, position, letter) :
    should_be_here = True

    for x in arr :
        if x["letter"] == letter :
            if x["non_pos"].count(position) > 0 :
                should_be_here = False
                break
    
    return should_be_here


## Checks if a letter is in a word and returns true or false

def check_letter_in_word(word, letter) :
    if letter in word :
        return True
    else :
        return False

def determine_probability(words_arr) :
    num_list = open("num_list.txt", "r")
    short_list = open("short_list.txt", "r")

    popularity_arr = json.loads(num_list.read())
    short_list_length = len(short_list.readlines())
    letter_probabilities = {}
    word_probabilities = {}

    for item in popularity_arr.items() :
        letter_probabilities[item[0]] = (item[1] / short_list_length)

    for word in words_arr :
        word_prob = 0

        for letter in word :
            word_prob += letter_probabilities[letter]

        word_probabilities[word] = word_prob
    
    ordered_probabilities = sorted(word_probabilities.items(), reverse=True, key=lambda item:item[1])

    num_list.close()
    short_list.close()

    return list(ordered_probabilities)[0]

def check_tester_word(correct_word, guesssed_word) :
    test_answer_arr = [0, 0, 0, 0, 0]

    for i in range(len(guesssed_word)) :
        if guesssed_word[i] in correct_word :
            test_answer_arr[i] = 1
        
        if guesssed_word[i] == correct_word[i] :
            test_answer_arr[i] = 2

    return test_answer_arr


def analyse_test_results() :
    testing_file = open("testing_list.txt", "r")
    lines = testing_file.readlines()

    total_words = len(lines)
    success_rate = total_words / 100
    total_tries = 0
    average_tries = 0

    for x in lines :
        total_tries += json.loads(x)["tries"]
    
    average_tries = round(total_tries / total_words, 2)

    print(average_tries)





## Loops until it guesses the correct word
# Asks for input each time
## *** NEED ALLOWANCES TO BE ABLE TO ENTER A CUSTOM WORD ***

def recurrent_guesses(last_word_guessed) :
    last_word = last_word_guessed
    letter_order = ["", "", "", "", ""]
    letters_included = []
    letters_included_non_positions = []
    letters_not_included = []
    word_file = open("short_list.txt", "r")
    word_list = word_file.readlines()
    possible_words = []
    try_counter = 0

    ##### FOR TESTING ONLY #####

    list_file = open("short_list.txt", "r")
    list_of_words = list_file.readlines()
    tester_word = list_of_words[random.randint(0, len(list_of_words) - 1)].strip()
    list_file.close()

    l1 = 0
    l2 = 0
    l3 = 0
    l4 = 0
    l5 = 0

    while((l1 + l2 + l3 + l4 + l5) != 10) :
        
        ## Handling Inputs

        # l1 = int(input("First Letter Progress: "))
        # l2 = int(input("Second Letter Progress: "))
        # l3 = int(input("Third Letter Progress: "))
        # l4 = int(input("Fourth Letter Progress: "))
        # l5 = int(input("Fifth Letter Progress: "))

        # letters_arr = [l1, l2, l3, l4, l5]

        ##### FOR TESTING ONLY #####

        letters_arr = check_tester_word(tester_word, last_word)

        l1 = letters_arr[0]
        l2 = letters_arr[1]
        l3 = letters_arr[2]
        l4 = letters_arr[3]
        l5 = letters_arr[4]

        ## Turning inputs into letters not included, letters included, and letters in the correct spot

        for x in range(len(letters_arr)) :
            if letters_arr[x] == 1 :

                if last_word[x] not in letters_included :
                    letters_included.append(last_word[x])
                    
                if not check_and_add_non_position(letters_included_non_positions, x, last_word[x]) :
                    letters_included_non_positions.append({"letter": last_word[x], "non_pos": [x]})
                

            elif letters_arr[x] == 2 :
                letter_order[x] = last_word[x]

                if last_word[x] not in letters_included :
                    letters_included.append(last_word[x])

            elif letters_arr[x] == 0 :
                letters_not_included.append(last_word[x])

        ## Check Letters in Different Spot
        ## *** NEED ALLOWANCES FOR DOUBLE LETTERS ***

        if len(letters_included) != 0 : 
            for w in word_list :
                check_arr = []
                word = w.strip()
                
                for l in letters_included :
                    check_arr.append(check_letter_in_word(word, l))
                    check_arr.append(check_letter_not_in_position(letters_included_non_positions, check_for_index(word, l), l))
                
                if all(check_arr) and check_for_index(possible_words, word) == -1:
                    possible_words.append(word)
                elif not all(check_arr) and check_for_index(possible_words, word) != -1:
                    possible_words.remove(word)
        else :
            possible_words = word_list


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
        
        # print(possible_words)
        # print(str(len(possible_words)) + " words found.")
        # print(letters_included_non_positions)

        try :
            last_word = determine_probability(possible_words)[0]
            # print(last_word)    
            try_counter += 1
        except :
            print("Sorry, there are currently no words matching those parameters.")
            break
    
    if (l1 + l2 + l3 + l4 + l5) == 10 :
        print("Congratulations, you solved it in " + str(try_counter) + " tries!")
        testing_list_file = open("testing_list.txt", "a+")
        testing_list_file.write(json.dumps({"word": last_word, "tries": try_counter}) + "\n")
        testing_list_file.close()

    word_file.close()


## Generates a random word, for testing 

def generate_random_word() :
    five_letter_words = open("short_list.txt", "r")
    list_of_words = five_letter_words.readlines()
    random_num = random.randint(0, len(list_of_words) - 1)
    five_letter_words.close()

    return list_of_words[random_num].strip()

def conduct_testing() :
    testing_counter = 0

    while(testing_counter < 100) :
        start_word = first_guess()
        recurrent_guesses(start_word)
        testing_counter += 1

    analyse_test_results()


## Starts off the guessing 
# print("Random Word: " + generate_random_word())

# conduct_testing()


# determine_probability(['hello', 'feats', 'green'])



    



