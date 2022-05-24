from tools import tplComp, loadTemplates
templates = loadTemplates()
print(tplComp(templates['screenshot'], templates['in_client']))