text = open('fairytales4.txt', 'r', encoding='utf-8')


def reformat_line(line):

    line = '<title>{}</title>'.format(line[:-1].title())
    return line

with open('fairytales4_reformatted.txt', 'w', encoding='utf-8') as outp:

    tale = ''

    for i, line in enumerate(text):
        line = line.strip()
        if tale == '' and line.startswith('<title>'):
        # if tale == '' and line.isupper() and line.endswith('.'):
            outp.write(line.strip() + '\n')
            # outp.write(reformat_line(line) + '\n')
        elif tale != '' and line.startswith('<title>'):
        # elif tale != '' and line.isupper() and line.endswith('.'):
            outp.write(tale + '\n\n')
            tale = ''
            outp.write(line.strip() + '\n')
            # outp.write(reformat_line(line) + '\n')
        else:
            tale += line.strip()
    outp.write(tale + '\n\n')

text.close()