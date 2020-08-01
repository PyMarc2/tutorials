username = "Hello"
count = 0

while count < 5:
    password = input("Enter Password: ")

    if username == "Hello" and password == "Turtle":
        print("Access Granted ")
        break

    else:
        print("Access Denied ")
        count += 1
