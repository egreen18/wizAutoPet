from tools import checkGen, loadTemplates, osResGen
os_res = 'temp'
templates = loadTemplates(os_res)
while ~checkGen(templates['dance']):
    print('unidentified')
    while checkGen(templates['dance']):
        print('identified')