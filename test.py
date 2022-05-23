from tools import checkGen, loadTemplates
templates = loadTemplates()
while not checkGen(templates['no_snack']):
    print('unidentified')
while checkGen(templates['no_snack']):
    print('identified')