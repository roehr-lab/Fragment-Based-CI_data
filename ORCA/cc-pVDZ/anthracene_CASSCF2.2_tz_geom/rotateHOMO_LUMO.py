import numpy as np

AOtoMO = np.loadtxt("AOtoMO.csv", delimiter=",")
Occupations = np.loadtxt("Occupations.csv", delimiter=",")

indices = []
for i, occ in enumerate(Occupations):
    if np.allclose(occ,1.0):
        indices.append(i)
print(indices)
# AOtoMO[AO,MO]
assert len(indices) == 2
#mo switch
temp = np.copy(AOtoMO[:,indices[0]])
AOtoMO[:,indices[0]] = AOtoMO[:,indices[1]]
AOtoMO[:,indices[1]] = temp
print(AOtoMO[:,indices])
np.savetxt("AOtoMO.csv", AOtoMO, delimiter=",")
