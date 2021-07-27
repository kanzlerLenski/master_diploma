text = open('all_tales.txt', 'r', encoding='utf-8')

titles = []

with open('tales_deduped.txt', 'w', encoding='utf-8') as outp:

    for line in text:
        if line.startswith('<title>') and line not in titles:
            titles.append(line)
            outp.write(line)
            outp.write(next(text))