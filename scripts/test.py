fields = {"pattern 1": "replacement text 1", "pattern 2": "replacement text 2"}

with open('yourfile.txt', 'w+') as f:
    s = f.read()
    for key in fields:
        s = s.replace(key, fields[key])
    f.write(s)