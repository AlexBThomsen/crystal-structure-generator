# Crystal Structure Generator

A Python script for generating common crystal structures using the Atomic Simulation Environment (ASE).

## Features

- Generates common crystal structures:
  - Face-Centered Cubic (FCC)
  - Body-Centered Cubic (BCC)
  - Hexagonal Close-Packed (HCP)
- Supports multiple elements with default parameters
- Configurable supercell size
- JSON output compatible with the atomic structure visualizer
- Comprehensive input validation
- Unit tests

## Supported Elements

### FCC Structures
- Copper (Cu): a = 3.61 Å
- Aluminum (Al): a = 4.05 Å
- Nickel (Ni): a = 3.52 Å
- Platinum (Pt): a = 3.92 Å
- Gold (Au): a = 4.08 Å
- Silver (Ag): a = 4.09 Å

### BCC Structures
- Iron (Fe): a = 2.87 Å

### HCP Structures
- Titanium (Ti): a = 2.95 Å, c/a = 1.587
- Zinc (Zn): c/a = 1.856
- Magnesium (Mg): c/a = 1.624

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Generate Common Structures
```bash
python generate_common_structures.py
```
This will generate JSON files for FCC (Cu), BCC (Fe), and HCP (Ti) structures.

### Using in Python Code
```python
from generate_common_structures import generate_structure

# Generate a 2x2x2 FCC copper structure
cu_fcc = generate_structure('Cu', 'fcc', 3.61, (2, 2, 2))

# Generate a BCC iron structure with default parameters
fe_bcc = generate_structure('Fe', 'bcc')

# Generate an HCP titanium structure
ti_hcp = generate_structure('Ti', 'hcp', 2.95, c_over_a=1.587)
```

### Running Tests
```bash
python -m unittest test_generate_common_structures.py
```

## Output Format

The generated JSON files contain:
- `positions`: List of atomic positions [x, y, z]
- `numbers`: List of atomic numbers
- `cell`: 3x3 matrix defining the unit cell
- `pbc`: Periodic boundary conditions
- `metadata`: Structure information including:
  - element
  - structure type
  - lattice constant
  - c/a ratio (for HCP)
  - number of atoms
  - supercell size

## Error Handling

The script includes comprehensive input validation:
- Validates element symbols
- Checks structure types
- Ensures positive lattice constants
- Validates supercell dimensions
- Requires c/a ratio for HCP structures

## Definitions
- `ATOMIC_NUMBERS`: Atomic numbers for elements
- `LATTICE_CONSTANTS`: Default lattice parameters
- `HCP_C_OVER_A`: Default c/a ratios for HCP structures 