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


def hashing(str1):
    line_byte = str1.encode()                   # str --> byte
    hash_obj = hashlib.sha256(line_byte)        # hash
    return hash_obj.hexdigest()


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
        d[k].append(v)                          # [(1, [Bp, Bp, Bp]), (2, [Vp, Vp]), (3, [Sz])]
    list(d.items())

    file = open("client_input.txt", "r")
    data = file.readlines()                     # client input

    for line in data:
        hex_dig = hashing(line)
        print("\n-------------------------------------------")
        print("Client input hash-prefix:")
        print(hex_dig[0:10])                    # prefix - first 10 characters

        print("\nLongest sub-string matches in server data:")
        max_var = 0
        max_hash = ""
        for v in d.values():                    # longest sub-string match between client and server data
            for x in v:
                temp = longest_substring(hex_dig[0:10], x)
                if temp.size > max_var:         # longest match size
                    max_var = temp.size
                    max_hash = x                # which server-element has the longest match size

        print("\nLongest match size + in which element:")
        print(max_var)
        print(max_hash)

        max_freq = 0
        for v in d.values():                    # counting the frequency of longest-matching data
            for x in v:
                if x == max_hash:
                    max_freq += 1
        print("\nFrequency of longest-matching element:")
        print(max_freq)

        for k, v in d.items():                  # finding the category of longest-matching data
            if v[0] == max_hash:
                print("\nCategory of longest-matching element:")
                print(k)

                if max_hash == hex_dig:         # if client side data matches server side data totally
                    print("\nComplete match! - data already exists")
                    print("Adding client input to server side...")
                    d[k].append(hex_dig)
                    print("New server database elements:")
                    print(list(d.items()))
                else:
                    print("\nNo complete match!")
                    print("Adding client input to server side...")
                    d[k].append(hex_dig)
                    print("New server database elements:")
                    print(list(d.items()))
