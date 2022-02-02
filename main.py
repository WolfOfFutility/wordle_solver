import json
import random

def find_all_5_letter_words() :
    f = open("all_words.txt", "r")
    w = open("short_list.txt", "a")

    for x in f :
        if len(x) == 6 :
            w.write(x)

    f.close()
    w.close()



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

def first_guess() :
    first_words = open("first_words.txt", "r")
    content = first_words.readlines()
    random_num = random.randint(0, len(content) - 1)
    starter_word = content[random_num].strip()

    print("First Guess: " + starter_word)
    first_words.close()

    return starter_word

def check_for_index(arr, element) :
    try :
        index = arr.index(element)
        return index
    except :
        return -1

def recurrent_guesses(last_word_guessed, current_word) :
    last_word = last_word_guessed
    letter_order = ["", "", "", "", ""]
    letters_included = []
    letters_not_included = []
    word_file = open("short_list.txt", "r")
    word_list = word_file.readlines()

    l1 = 0
    l2 = 0
    l3 = 0
    l4 = 0
    l5 = 0

    while((l1 + l2 + l3 + l4 + l5) != 10) :
        possible_words = []

        l1 = int(input("First Letter Progress: "))
        l2 = int(input("Second Letter Progress: "))
        l3 = int(input("Third Letter Progress: "))
        l4 = int(input("Fourth Letter Progress: "))
        l5 = int(input("Fifth Letter Progress: "))

        letters_arr = [l1, l2, l3, l4, l5]

        for x in range(len(letters_arr)) :
            if letters_arr[x] == 1 and last_word[x] not in letters_included :
                letters_included.append(last_word[x])
            elif letters_arr[x] == 2 :
                letter_order[x] = last_word[x]
            elif letters_arr[x] == 0 :
                letters_not_included.append(last_word[x])

        ## After first iteration check current list of words

        print('Letters Order: ' + str(letter_order))
        print('Included Letters: ' + str(letters_included))

        ## Check Letters in Different Spot
        for k in letters_included :
            for w in word_list :
                if k in w :
                    possible_words.append(w.strip())
            for l in possible_words :
                if k not in l and check_for_index(possible_words, l) > 0 :
                    possible_words.remove(l)

        ## Check Guaranteed Letters
        for w in word_list :
            pass
            


        for o in letter_order :
            for w in word_list :
                if check_for_index(w.strip(), o) == check_for_index(letter_order, o) and check_for_index(possible_words, w.strip()) < 0 :
                    possible_words.append(w.strip())
                else :
                    if check_for_index(possible_words, w.strip()) > 0 :
                        possible_words.remove(w.strip())

        # for i in word_list :
        #     for j in letter_order :
        #         if check_for_index(i.strip(), j) == check_for_index(letter_order, j) and check_for_index(possible_words, i.strip()) < 0 :
        #             possible_words.append(i.strip())
        #         else :
        #             if check_for_index(possible_words, i.strip()) > 0 :
        #                 possible_words.remove(i.strip())

        ## Check Letters Not Included
        for m in letters_not_included :
            for w in possible_words :
                if m in w :
                    possible_words.remove(w)

        last_word = possible_words[random.randint(0, len(possible_words) - 1)]

        print(possible_words)

        print("Word to get: " + current_word)
        print(last_word)    

def generate_random_word() :
    five_letter_words = open("short_list.txt", "r")
    list_of_words = five_letter_words.readlines()
    random_num = random.randint(0, len(list_of_words) - 1)
    five_letter_words.close()

    return list_of_words[random_num].strip()

# first_guess()
# while(first_letter_progress == 0 and second_letter_progress == 0 and third_letter_progress == 0 and fourth_letter_progress == 0 and fifth_letter_progress == 0) :
#     recurrent_guesses()

current_word = generate_random_word()

print("Word to get: " + current_word)

start_word = first_guess()

recurrent_guesses(start_word, current_word)



    



