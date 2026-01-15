# Fragment-Based Configuration Interaction

This repository contains the core data associated with the research paper:

**Fragment-Based Configuration Interaction: Towards a Unifying Description of Biexcitonic Processes in Molecular Aggregates**

## 📄 Overview

The data produced by the calculations.

## 💾 Hamiltonian Data Access

Due to the high dimensionality and significant file size of the Hamiltonian objects (`realH.parquet`), these files are not uploaded to this GitHub repository.

These objects are available upon request for researchers interested in reproducing the results or performing further analysis. Please reach out to:

**Johannes Adelperger**  
📧 johannes.adelperger@uni-wuerzburg.de  
📍 University of Würzburg

## 🛠 Repository Structure

- **`NOCI/`**: Data related to Non-Orthogonal Configuration Interaction calculations.
- **`ORCA/`**: Input and processed output from ORCA quantum chemistry packages.
- **`SymbolicCI/`**: Data related toSymbolicCI calculations.

## 🚀 Data Compression & Optimization

To handle the massive datasets involved in this project, the following optimizations were applied to all `.parquet` files:

- **Thresholding**: Values with an absolute magnitude $< 10^{-10}$ were set to zero to enhance sparsity.
- **Symmetry**: For symmetric Hamiltonian matrices, only the upper triangle is stored to reduce the disk footprint by ~50%.
- **Compression**: Files are compressed using the Zstandard (zstd) algorithm at maximal compression levels.

### Reconstructing the Matrices

If you have obtained the `realH.parquet` files, you can reconstruct the full symmetric matrix in Python using the following code:

```python
import pandas as pd
import numpy as np

def load_hamiltonian(path):
    """
    Loads an optimized upper-triangular Parquet file and 
    reconstructs the full symmetric matrix.
    """
    df = pd.read_parquet(path)
    matrix = df.to_numpy()
    
    # Mirror the upper triangle to the lower triangle
    # We subtract the diagonal once because it's included in both matrix and matrix.T
    full_matrix = matrix + matrix.T - np.diag(matrix.diagonal())
    return full_matrix
```