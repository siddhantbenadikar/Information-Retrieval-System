# Importing libraries
import os
import re

# Defining global variables
all_files = []
directory = 'Stemmed_corpus'


# Function to remove noise and punctuations from the stemmed cacm docs and generate corpus
def get_content():
    filename = 'cacm_stem.txt'

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(filename, 'r') as f:
        content = f.read()
        content = content.lower().replace('\n', ' ')
        content = re.split(r'#\s[0-9]*', content)
        i = 1
        for items in content[1:]:
            if ' pm ' in items:
                items = items.split(' pm ')[0]
                items += " pm"
            elif 'pm ' in items:
                items = items.split('pm ')[0]
                items += " pm"
            elif 'pmb ' in items:
                items = items.split('pmb ')[0]
                items += " pm"
            elif ' am ' in items:
                items = items.split(' am ')[0]
                items += " am"

            with open(directory + '/CACM-' + str(i).zfill(4) + '.txt', 'w+') as f:
                f.write(items)
                f.close()
            i += 1
