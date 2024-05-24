with open("dictionary.txt", "r") as file:
    content = file.read()

content_uppercase = content.upper()

with open("dictionary.txt", "w") as file:
    file.write(content_uppercase)
