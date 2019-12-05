# Anonimize

__2019__

Proof of Concept implementation
* No real client-server communication; client input in file
* Client-side anonymization
* Converts hierarchical attributes to categorical
* Satisfies k-anonymity

__USAGE__

For different test cases, client input files need to be modified:

In my PoC environment, at first glance...

client_hierarchical_input.txt holds the name of the client's town (residence)

client_categorical_input.txt holds the client's gender

client_numerical_input.txt holds the client's age

client_sensitive_input.txt holds the client's medical condition

To be able to test modules separately, there is no real connection between the two algorithms.

1. Execute Attribute_convert.py - maps client's hierarchical attributes to categorical ones

    1.1 Uses client_hierarchical_input.txt
    
    1.2 Modifies client_categorical_input.txt - important to always reset to its original condition before rerunning the algorithm

2. Execute Anonimize.py - builds k-anonymous database 

    2.1 Uses client_categorical_input.txt, client_numerical_input.txt and client_sensitive_input.txt
    
