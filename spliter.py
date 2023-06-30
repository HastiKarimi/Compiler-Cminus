# read rules.txt and give me the words starting with '#' and put them in a list

with open('rules.txt', 'r') as f:
    rules = f.readlines()

rules = [x.strip().split(" ") for x in rules]
words = []
for i in range(len(rules)):
    for x in rules[i]:
        if x.startswith('#'):
            words.append(x[1:])

words = set(words)
for word in words:
    print(word)
