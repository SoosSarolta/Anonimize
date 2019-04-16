import hashlib
from collections import defaultdict
from difflib import SequenceMatcher


def longest_substring(str1, str2):              # algorithm for finding longest common substring
    seq_match = SequenceMatcher(None, str1, str2)
    match = seq_match.find_longest_match(0, len(str1), 0, len(str2))
    if match.size == 0:
        print("No common sub-string found!")
    else:
        print(str1[match.a: match.a + match.size])
    return match


def hashing(str1):                              # client input hashing algorithm
    line_byte = str1.encode()                   # str --> byte
    hash_obj = hashlib.sha256(line_byte)        # hash
    return hash_obj.hexdigest()


def characters_to_send(dic, mylist, sending):   # server telling how many characters to send to get unambiguous answer
    for values in dic.values():                 # only works fine if we send data that already exists in server-database
        for valuePart in values:
            mylist.append(valuePart)
    for list_i in range(len(mylist) - 1):
        for list_j in range(len(mylist) - 1):   # TODO opti - ne hasonlítson össze mindent mindennel újra és újra
            if mylist[list_i] != mylist[list_j + 1]:
                for char in range(1, 65):
                    if mylist[list_i][0:char] not in mylist[list_j + 1]:
                        sending.append(char)
                        break


def frequency(dic, hash_max):                   # counting the frequency of longest-matching data
    freq_max = 0
    for values in dic.values():
        for valuePart in values:
            if valuePart == hash_max:
                freq_max += 1
    print("\nFrequency of longest-matching element:")
    print(freq_max)
    return freq_max


def category(dic, hash_max, hexa_dig):          # finding the category of longest-matching data
    for keys, values in dic.items():
        if values[0] == hash_max:
            print("\nCategory of longest-matching element:")
            print(keys)

            if hash_max == hexa_dig:            # if client side data matches server side data totally
                print("\nComplete match! - data already exists")
                print("Adding client input to server side...")
                dic[keys].append(hexa_dig)
                print("New server database elements:")
                print(list(dic.items()))
            else:                               # if client side data doesn't match server side data totally
                print("\nNo complete match!")
                print("Adding client input to server side...")
                dic[keys].append(hexa_dig)
                print("New server database elements:")
                print(list(dic.items()))


def longest_match(dic, hexa_dig, min_chars, sizes, max_variable, mylist):
    list_of_temp = []
    hash_max = ""

    for values in dic.values():                 # searching longest sub-string matches between client and server data
        for valuePart in values:
            temporary = longest_substring(hexa_dig[0:min_chars], valuePart)
            sizes.append(temporary.size)
            list_of_temp.append(temporary)

    for values in dic.values():                 # how many characters to send to get unambiguous answer
        for _ in values:                        # in case of data not seen before
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

            if temporary.size > max_variable:  # longest match size
                max_variable = temporary.size
                hash_max = valuePart           # which server-element has the longest match size

    print("\nLongest match size + in which element:")
    print(max_variable)
    print(hash_max)

    return hash_max                             # TODO innen a 80-as sorra ugrik?!


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
        d[k].append(v)                          # result: [(1, [Bp, Bp, Bp]), (2, [Vp, Vp]), (3, [Sz])]
    list(d.items())

    file = open("client_input.txt", "r")
    data = file.readlines()                     # client input

    for line in data:
        charsToSend = []
        matchSizes = []
        temp_list = []
        max_var = 0

        hex_dig = hashing(line)                 # hashing input
        print("\n-------------------------------------------")
        print("Client input hash-prefix:")

        characters_to_send(d, temp_list, charsToSend)
        minChars = max(charsToSend)             # choose characters to send
        print(hex_dig[0:minChars])              # prefix of input - first n characters

        print("\nLongest sub-string matches in server data:")
        max_hash = longest_match(d, hex_dig, minChars, matchSizes, max_var, temp_list)

        max_freq = frequency(d, max_hash)       # longest-matching data frequency
        category(d, max_hash, hex_dig)          # longest-matching data category
