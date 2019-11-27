if __name__ == '__main__':

    # equivalence classes on the server
    # [ID, Age, Gender, Residence, Item number, Safe or not]
    server_equivalence_classes = [
        (1, range(40, 51), "Male", "1", 3, True),
        (2, range(20, 31), "Male", "2", 5, True),
        (3, range(20, 31), "Female", "1", 2, False)
    ]

    # sensitive information table on the server
    # [EQ-class ID, Condition]
    server_sensitive_info = [
        (2, "Leukemia"),
        (2, "Lung cancer"),
        (1, "Knee cyst"),
        (2, "Stomach ulcer"),
        (1, "Sore throat"),
        (1, "Shoulder sprain"),
        (2, "Arthritis"),
        (2, "Kidney stone")
    ]

    # client input from file (categorical attributes)
    file_categorical = open("client_categorical_input.txt", "r")
    categorical_attr = file_categorical.readline().strip()

    # client's categorical attributes are sent to the server (in this e.g.: gender and residence)
    attrs = categorical_attr.split(";")
    gender = attrs.__getitem__(0)
    residence = attrs.__getitem__(1)

    print("\n-----------------------------------------------------")
    print("Client's categorical attributes:")
    print("Gender - " + gender + "\nResidence - " + residence)
    print("-----------------------------------------------------")

    not_fitting_eq_classes_num = 0

    # if server has suitable equivalence class for client's categorical data, it is sent back to the client
    for eq_class in server_equivalence_classes:
        if eq_class.__contains__(gender) & eq_class.__contains__(residence):
            print("\nA suitable EQ-class for categorical data on the server:")
            print(list(eq_class))

            # client input from file (numerical attributes)
            file_numerical = open("client_numerical_input.txt", "r")
            age = int(file_numerical.readline().strip())

            print("\n-----------------------------------------------------")
            print("Client's numerical attributes:")
            print("Age - " + str(age))
            print("-----------------------------------------------------")

            # client checks the hit list, if there's a suitable class for its numerical data too
            if age in eq_class[1]:
                print("\nA suitable EQ-class for both categorical and numerical data on the server:")
                print(list(eq_class))

                # if there is a class that fits, client gets added to it (item number rises by 1)
                eq_class_as_list = list(eq_class)
                eq_class_as_list[4] += 1
                if eq_class_as_list[4] >= 3:
                    eq_class_as_list[5] = True
                print("\nClient added to the chosen EQ-class:")
                print(eq_class_as_list)

                # if the chosen equivalence class has minimum k elements, client sends its sensitive data to the server
                if eq_class_as_list[5]:
                    server_sensitive_info_as_list = list(server_sensitive_info)

                    # client input from file (sensitive attributes)
                    file_sensitive = open("client_sensitive_input.txt", "r")
                    condition = file_sensitive.readline().strip()

                    new_sensitive_info_tuple = (eq_class_as_list[0], condition)
                    server_sensitive_info_as_list.append(new_sensitive_info_tuple)

                    print("\nClient's sensitive data added:")
                    print(server_sensitive_info_as_list)

                # else, client stores its sensitive data and waits till the class's safe flag becomes true

            # if client doesn't find a suitable class for its numerical data in the hit list, tells the server
            else:
                print("\nNo suitable EQ-class for both categorical and numerical data on the server!")
                print("Please create a new one! Standard interval size on the server:")

                # server sends standard interval size to client and asks to create a new class with the help of it
                server_interval_size = len(eq_class[1])
                print(server_interval_size - 1)

                # client generates its own new equivalence class and sends it to the server
                my_age_range = range(age - 5, (age - 5) + server_interval_size)

                my_equivalence_class = (4, my_age_range, gender, residence, 1, False)

                server_equivalence_classes_as_list = list(server_equivalence_classes)
                server_equivalence_classes_as_list.append(my_equivalence_class)

                print("\nClient's new equivalence class added:")
                print(server_equivalence_classes_as_list)
        else:
            not_fitting_eq_classes_num += 1

    # if server has no suitable equivalence class for client's categorical data
    if not_fitting_eq_classes_num == server_equivalence_classes.__len__():
        print("\nNo suitable EQ-class for categorical data on the server!")
        print("Please create a new one! Standard interval size on the server:")

        # server sends standard interval size to client and asks to create a new class with the help of it
        server_interval_size = len(server_equivalence_classes[0][1])
        print(server_interval_size - 1)

        # client input from file (numerical attributes)
        file_numerical = open("client_numerical_input.txt", "r")
        age = int(file_numerical.readline().strip())

        # client generates its own new equivalence class and sends it to the server
        my_equivalence_class = (4, range(age - 5, (age - 5) + server_interval_size), gender, residence, 1, False)

        server_equivalence_classes_as_list = list(server_equivalence_classes)
        server_equivalence_classes_as_list.append(my_equivalence_class)

        print("\nClient's new equivalence class added:")
        print(server_equivalence_classes_as_list)
