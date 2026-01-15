import numpy as np
import os

aggregate_shift_x = 0.
aggregate_shift_y = 0.
aggregate_shift_z = 3.5

fragment_name = 'ethene'
fragment_file = 'ethene.frag'

settings = {}
settings['nthreads'] = '40'
settings['BasisSet'] = '/home/jgreiner/BasisSets/cc-pvtz.json'
settings['savingHamiltonian'] = 'True'
settings['doCorrelationCorrection'] = 'False'
settings['nroots'] = '200'
settings['maxExcitations'] = '2'
settings['maxPathway'] = '1'
settings['printDiabaticStates'] = 'True'

path_to_results = '/home/jgreiner/Promotion/MethodPaper/cc-pvtz/ethene_HJ_noCorrelation/results'
path_to_fragmentfile = '/home/jgreiner/Promotion/MethodPaper/cc-pvtz/ethene_HJ_noCorrelation/ethene.frag'
path_to_SymCI_sub = '/home/jgreiner/Promotion/MethodPaper/cc-pvtz/ethene_HJ_noCorrelation/SymbolicCI.sub'

def generate_input_file(file, nmer, shift_x=0., shift_y=0., shift_z=0.):
    """
    Generates the input file for the aggregate calculator.
    """
    with open(file, 'w') as f:
        for key, value in settings.items():
            f.write(f'{key} = {value}\n')

        f.write(f'\n* {fragment_name} fragmentfile\n')
        f.write(f'file = {fragment_file}\n')
        f.write(f'end\n\n')

        f.write(f'&\n')
        for n in range(nmer):
            f.write(f'{fragment_name} {(aggregate_shift_x+shift_x)*n:10.6f} {(aggregate_shift_y+shift_y)*n:10.6f} {(aggregate_shift_z+shift_z)*n:10.6f}\n')
        f.write(f'end\n')

def prepare_symbolicCI(path, filename):
    os.system(f'cd {path}; cp {path_to_SymCI_sub} .')
    print(f'cd {path}; sbatch SymbolicCI.sub; cd -')

def make_calculations(nmer, x_shifts = np.array([0.]), y_shifts = np.array([0.]), z_shifts = np.array([0.])):
    """
    Makes the calculations for the given range of nmer.
    """
    x_shifts, y_shifts, z_shifts = np.meshgrid(x_shifts, y_shifts, z_shifts, indexing='ij')
    x_shifts = x_shifts.flatten()
    y_shifts = y_shifts.flatten()
    z_shifts = z_shifts.flatten()

    os.makedirs(path_to_results, exist_ok=True)
    for i in range(len(x_shifts)):
        x_shift = x_shifts[i]
        y_shift = y_shifts[i]
        z_shift = z_shifts[i]
        aggregate_path = os.path.join(path_to_results, f'{nmer}-{i}')
        os.makedirs(aggregate_path, exist_ok=True)
        input_file_name = 'SymCI.inp'
        input_file = os.path.join(aggregate_path,input_file_name)
        generate_input_file(input_file, nmer, x_shift, y_shift, z_shift)
        os.system(f'cp {path_to_fragmentfile} {os.path.join(aggregate_path, fragment_file)}')
        prepare_symbolicCI(aggregate_path, input_file_name)
        print(f'Finished calculation for {nmer} fragments with shift {x_shift:4.2f}, {y_shift:4.2f}, {z_shift:4.2f}.')

if __name__ == '__main__':
    n_mer = 15
    x_shifts = np.arange(0, 6.1, 0.1)
    np.savez("x_shifts", x_shifts = x_shifts)
    make_calculations(n_mer, x_shifts=x_shifts)



