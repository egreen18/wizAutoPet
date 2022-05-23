from tools import checkGen, loadTemplates
templates = loadTemplates()
while ~checkGen(templates['match']):
    print('unidentified')
    while checkGen(templates['match']):
        print('identified')