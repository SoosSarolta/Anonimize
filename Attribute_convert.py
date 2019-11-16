import hashlib
import random
from collections import defaultdict
from difflib import SequenceMatcher

# import numpy


# client input hashing algorithm
def hashing(str1):
    line_byte = str1.encode()                        # str --> byte
    hash_obj = hashlib.sha256(line_byte)
    return hash_obj.hexdigest()


# finding longest common substring
def longest_substring(str1, str2):
    seq_match = SequenceMatcher(None, str1, str2)
    match = seq_match.find_longest_match(0, len(str1), 0, len(str2))
    if match.size == 0:
        print("No common sub-string found!")
    return match


# searching longest sub-string matches between client data and server data
def longest_match(dic, hexa_dig, min_chars, sizes, max_variable, mylist):
    list_of_temp = []
    hash_max = ""

    for values in dic.values():                     # iterating through server data
        for valuePart in values:
            temporary = longest_substring(hexa_dig[0:min_chars], valuePart)  # finding longest common substring
            sizes.append(temporary.size)            # match - how many characters long
            list_of_temp.append(temporary)          # longest common substrings between client input and all server row

    for values in dic.values():                     # how many characters to send to get unambiguous answer
        for _ in values:                            # in case of data not seen before
            for ii in range(len(mylist) - 1):
                for jj in range(len(mylist) - 1):
                    if mylist[ii] != mylist[jj + 1] and sizes[ii] == sizes[jj + 1]:
                        if max(sizes) == sizes[ii]:
                            sizes.clear()
                            print("\nTrying again with one more characters...")
                            longest_match(dic, hexa_dig, min_chars+1, sizes, max_variable, mylist)

    i = 0
    for values in dic.values():
        for valuePart in values:
            temporary = list_of_temp[i]
            i += 1

            if temporary.size > max_variable:       # longest match size
                max_variable = temporary.size
                hash_max = valuePart                # which server-element has the longest match size

    print("\nLongest-matching element:")
    print(hash_max)

    return hash_max


# server telling how many characters to send to get unambiguous answer in case of data seen before
def characters_to_send(dic, mylist, sending):
    temp = 0
    flag = 0

    for values in dic.values():
        for valuePart in values:
            mylist.append(valuePart)
    for list_i in range(len(mylist) - 1):
        if flag > 0:
            temp += 1
        flag += 1
        for list_j in range(temp, len(mylist) - 1):
            if mylist[list_i] != mylist[list_j + 1]:
                for char in range(1, 65):
                    if mylist[list_i][0:char] not in mylist[list_j + 1]:
                        sending.append(char)
                        break


# adding Laplace-noise to frequency to satisfy differential privacy
# def laplace_noise(freq):
#    random_l = numpy.random.laplace(0, 5, None)     # default: (0, 1, None)
#    if freq + round(random_l) <= 0:
#        return freq
#    else:
#        return freq + round(random_l)


# counting the frequency of longest-matching data
def frequency(dic, hash_max):
    freq_max = 0
    for values in dic.values():
        for valuePart in values:
            if valuePart == hash_max:
                freq_max += 1

#    diff_freq_max = laplace_noise(freq_max)

    return freq_max


# finding the category of longest-matching data
def category(dic, hash_max, hexa_dig):
    cat = 0

    for keys, values in dic.items():
        if values[0] == hash_max:
            print("\nCategory of longest-matching element:")
            print(keys)
            cat = keys

            if hash_max == hexa_dig:                # if client side data matches server side data totally
                print("\nComplete match! - data already exists")
                print("Adding client input to server side...")
                dic[keys].append(hexa_dig)
                print("New server database elements:")
                print(list(dic.items()))
            else:                                   # if client side data doesn't match server side data totally
                print("\nNot a complete match!")
                print("Adding client input to server side...")
                dic[keys].append(hexa_dig)
                print("New server database elements:")
                print(list(dic.items()))

    return cat


if __name__ == '__main__':

    server_data = [
        (1, "142f41284e5517e5e1e867854da66652d35da004dfe92cf5d1d93310ed32d98a"),    # Bp.
        (1, "142f41284e5517e5e1e867854da66652d35da004dfe92cf5d1d93310ed32d98a"),
        (1, "142f41284e5517e5e1e867854da66652d35da004dfe92cf5d1d93310ed32d98a"),
        (2, "6b68fb3d8a8f4e6fa1a6a6cb153cd82c914388e025e125bbdcdd110b0d146d9c"),    # Vp.
        (2, "6b68fb3d8a8f4e6fa1a6a6cb153cd82c914388e025e125bbdcdd110b0d146d9c"),
        (3, "7165c665e78d8aadbd53dd0607e9a5302f6c7ecb5f54071dd93a5f634b92571e")     # Szom.
    ]

    d = defaultdict(list)
    for k, v in server_data:
        d[k].append(v)                              # result: [(1, [Bp, Bp, Bp]), (2, [Vp, Vp]), (3, [Sz])]
    list(d.items())

    file = open("client_input.txt", "r")
    data = file.readlines()                         # client input in file

    for line in data:
        charsToSend = []
        matchSizes = []
        temp_list = []
        max_var = 0

        hex_dig = hashing(line)                     # hashing input
        print("\n-------------------------------------------")
        print("Client input hash-prefix:")

        characters_to_send(d, temp_list, charsToSend)
        minChars = max(charsToSend)                 # choose characters to send
        print(hex_dig[0:minChars])                  # prefix of input - first n characters

        max_hash = longest_match(d, hex_dig, minChars, matchSizes, max_var, temp_list)  # longest matching data
        max_freq = frequency(d, max_hash)           # longest-matching data frequency
        max_cat = category(d, max_hash, hex_dig)    # longest-matching data category
