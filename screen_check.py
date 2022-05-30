from tools import checkGen, loadTemplates
templates = loadTemplates()
while ~checkGen(templates['dance']):
    print('unidentified')
    while checkGen(templates['dance']):
        print('identified')