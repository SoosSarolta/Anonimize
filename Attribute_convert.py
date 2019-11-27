import hashlib
from collections import defaultdict
from difflib import SequenceMatcher

# import numpy


# client hashes its input
def hashing(str1):
    line_byte = str1.encode()                        # str --> byte
    hash_obj = hashlib.sha256(line_byte)
    return hash_obj.hexdigest()


# algorithm for finding longest common substring
def longest_substring(str1, str2):
    seq_match = SequenceMatcher(None, str1, str2)
    match = seq_match.find_longest_match(0, len(str1), 0, len(str2))
    if match.size == 0:
        print("No common sub-string found!")
    return match


# searching longest sub-string matches between client data and server data
def longest_match(server_table, client_hash, chars_to_be_sent, longest_substring_sizes,
                  longest_matching_hash_size, my_temp_list):
    help_list = []
    longest_matching_hash = ""

    # iterating through server-side database, searching for longest common substring
    # how many characters long is the match / finding longest common substrings between client input and all server row
    for values in server_table.values():
        for valuePart in values:
            temporary = longest_substring(client_hash[0:chars_to_be_sent], valuePart)
            longest_substring_sizes.append(temporary.size)
            help_list.append(temporary)

    # server telling the client how many characters to send to get unambiguous answer (in case of data not seen before)
    for values in server_table.values():
        for _ in values:
            for ii in range(len(my_temp_list) - 1):
                for jj in range(len(my_temp_list) - 1):
                    if my_temp_list[ii] != my_temp_list[jj + 1] and longest_substring_sizes[ii] == \
                            longest_substring_sizes[jj + 1]:
                        if max(longest_substring_sizes) == longest_substring_sizes[ii]:
                            longest_substring_sizes.clear()
                            print("\nTrying again with one more characters...")
                            longest_match(server_table, client_hash, chars_to_be_sent + 1, longest_substring_sizes,
                                          longest_matching_hash_size, my_temp_list)

    i = 0
    for values in server_table.values():
        for valuePart in values:
            temporary = help_list[i]
            i += 1

            # what is the longest match size and which server element has it
            if temporary.size > longest_matching_hash_size:
                longest_matching_hash_size = temporary.size
                longest_matching_hash = valuePart

    print("\nLongest-matching element:")
    print(longest_matching_hash)

    return longest_matching_hash


# server telling the client how many characters to send to get unambiguous answer (in case of data seen before)
def characters_to_send(server_table, my_temp_list, chars_to_be_sent):
    temp = 0
    flag = 0

    for values in server_table.values():
        for valuePart in values:
            my_temp_list.append(valuePart)
    for list_i in range(len(my_temp_list) - 1):
        if flag > 0:
            temp += 1
        flag += 1
        for list_j in range(temp, len(my_temp_list) - 1):
            if my_temp_list[list_i] != my_temp_list[list_j + 1]:
                for char in range(1, 65):
                    if my_temp_list[list_i][0:char] not in my_temp_list[list_j + 1]:
                        chars_to_be_sent.append(char)
                        break


# adding Laplace-noise to frequency to satisfy differential privacy
# def laplace_noise(freq):
#    random_l = numpy.random.laplace(0, 5, None)     # default: (0, 1, None)
#    if freq + round(random_l) <= 0:
#        return freq
#    else:
#        return freq + round(random_l)


# counting the frequency of longest-matching data
def frequency(server_table, longest_matching_hash):
    longest_match_frequency = 0
    for values in server_table.values():
        for valuePart in values:
            if valuePart == longest_matching_hash:
                longest_match_frequency += 1

#    diff_freq_max = laplace_noise(longest_match_frequency)

    return longest_match_frequency


# finding the category of longest-matching data
def category(server_table, longest_matching_hash, client_hash):
    longest_match_category = 0

    for keys, values in server_table.items():
        if values[0] == longest_matching_hash:
            print("\nCategory of longest-matching element:")
            print(keys)
            longest_match_category = keys

            # if client side data matches server side data totally
            if longest_matching_hash == client_hash:
                print("\nComplete match! - data already exists")
                print("Adding client input to server side...")
                server_table[keys].append(client_hash)
                print("New server database elements:")
                print(list(server_table.items()))

            # if client side data doesn't match server side data totally
            else:
                print("\nNot a complete match!")
                print("Adding client input to server side...")
                server_table[keys].append(client_hash)
                print("New server database elements:")
                print(list(server_table.items()))

    return longest_match_category


if __name__ == '__main__':

    # categorical attributes table on the server
    # [Category, Data]
    server_data = [
        (1, "142f41284e5517e5e1e867854da66652d35da004dfe92cf5d1d93310ed32d98a"),    # Bp.
        (1, "142f41284e5517e5e1e867854da66652d35da004dfe92cf5d1d93310ed32d98a"),
        (1, "142f41284e5517e5e1e867854da66652d35da004dfe92cf5d1d93310ed32d98a"),
        (2, "6b68fb3d8a8f4e6fa1a6a6cb153cd82c914388e025e125bbdcdd110b0d146d9c"),    # Vp.
        (2, "6b68fb3d8a8f4e6fa1a6a6cb153cd82c914388e025e125bbdcdd110b0d146d9c"),
        (3, "7165c665e78d8aadbd53dd0607e9a5302f6c7ecb5f54071dd93a5f634b92571e")     # Szom.
    ]

    server_data_as_dictionary = defaultdict(list)
    for k, v in server_data:
        server_data_as_dictionary[k].append(v)  # result: [(1, [Bp, Bp, Bp]), (2, [Vp, Vp]), (3, [Sz])]
    list(server_data_as_dictionary.items())

    # client input from file (hierarchical attributes)
    file_hierarchical = open("client_hierarchical_input.txt", "r")
    residence = file_hierarchical.readline().strip()

    longest_substring_search_match_sizes = []
    final_longest_match_size = 0
    chars_to_send = []
    temp_list = []

    # hashing client input
    hashed_client_input = hashing(residence)
    print("\n-------------------------------------------")
    print("Client input hash-prefix:")

    # choosing characters to send (prefix - first n characters)
    characters_to_send(server_data_as_dictionary, temp_list, chars_to_send)
    number_of_chars_to_send = max(chars_to_send)
    print(hashed_client_input[0:number_of_chars_to_send])

    # longest matching data, its frequency and category
    hash_of_longest_match = longest_match(server_data_as_dictionary, hashed_client_input, number_of_chars_to_send,
                                          longest_substring_search_match_sizes, final_longest_match_size, temp_list)
    frequency_of_longest_match = frequency(server_data_as_dictionary, hash_of_longest_match)
    category_of_longest_match = category(server_data_as_dictionary, hash_of_longest_match, hashed_client_input)

    # adding now categorical data to other categorical attributes
    file_categorical = open("client_categorical_input.txt", "a")
    file_categorical.write(";" + str(category_of_longest_match))
