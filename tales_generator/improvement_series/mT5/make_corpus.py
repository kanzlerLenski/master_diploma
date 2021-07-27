import os
import sys

with open(r'C:\Users\Eugene\PycharmProjects\tales_generator\experiments\improvement_series\mT5\tales_mt5_valid.txt', 'w', encoding='utf-8') as outp:
    for filename in os.listdir(r"{}".format(sys.argv[1])):
        if not filename.endswith('txt'):
            file = open(sys.argv[1] + "//" + filename, 'r', encoding='utf-8')
            prompt = ''
            text = ''
            for i, line in enumerate(file):
                line = line.replace('\n', ' ')
                if i < 4:
                    prompt += line
                else:
                    text += line
            outp.write('generate text:' + '\t' + prompt + '\t' + text + '\n')
        
                
        
        
            
