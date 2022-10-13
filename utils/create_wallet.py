def test(x):
    if x == 1:
        return True
    else:
        return False


a = test(0)

if a:
    print(True)
elif not a:
    print(False)
