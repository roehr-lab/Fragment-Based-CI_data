import numpy as np
import re
def parse_orca_output(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    num_basis_functions = None
    for line in lines:
        match = re.search(r' Basis Dimension        Dim             ....\s+(\d+)', line)
        if match:
            num_basis_functions = int(match.group(1))
            break

    if num_basis_functions is None:
        raise ValueError("Number of basis functions not found in the file")

    # Find the start of the molecular orbitals section
    start_index = None
    for i, line in enumerate(lines):
        if "MOLECULAR ORBITALS" in line:
            start_index = i

    if start_index is None:
        raise ValueError("MOLECULAR ORBITALS section not found in the file")

    
    occupation_numbers = []

    n_blocks = num_basis_functions // 6 + (num_basis_functions % 6 != 0)
    block_size = num_basis_functions + 4

    start_occ = start_index + 4
    for i in range(n_blocks):
        occupation_numbers.extend(map(float, lines[start_occ+i*block_size].split()))

    occupation_numbers = np.array(occupation_numbers)

    start_coeffs = start_index + 2

    # Parse the coefficients
    coefficients = []
    for i in range(num_basis_functions):
        coefficients.append([])
    for i in range(block_size*n_blocks):
        if i % block_size < 4:
            continue
        list_of_strings = []
        for sp in lines[start_coeffs+i].split()[2:]:
            if "-" in sp:
                for ind, spm in enumerate(sp.split('-')):
                    if ind == 0:
                        if spm == '':
                            continue
                        else:
                            list_of_strings.append(spm)
                        continue
                    list_of_strings.append('-'+spm)
            else:
                list_of_strings.append(sp)
        coefficients[i%block_size-4].extend(list(map(float, list_of_strings)))

    
    coefficients = np.array(coefficients)

    return coefficients, occupation_numbers

# Example usage
file_path = 'orca.out'
coefficients, occupation_numbers = parse_orca_output(file_path)
print("Coefficients Matrix:")
print(coefficients.shape)
np.savetxt('AOtoMO.csv', coefficients, delimiter=',')
print("Occupation Numbers Vector:")
print(occupation_numbers.shape)
np.savetxt('Occupations.csv', occupation_numbers, delimiter=',')
