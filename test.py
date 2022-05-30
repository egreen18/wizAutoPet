from tools import recordSequence, loadCoords, osResGen


os_res = osResGen()
coords = loadCoords(os_res)
memory = recordSequence(2,coords)

print(len(memory))