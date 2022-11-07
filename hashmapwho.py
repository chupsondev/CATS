for i in range(0, 10):
    if i == 5:
        raise Exception("Test")
    print(i)