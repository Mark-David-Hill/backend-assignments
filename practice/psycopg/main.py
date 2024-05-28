try:
    with open("examples.txt", "rt") as example_file:
        print(example_file.read())
except FileNotFoundError as e:
    print("Error: ", e, "Can't find file")
except IOError as e:
    print("Error: ", e)
