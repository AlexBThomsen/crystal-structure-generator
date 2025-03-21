"""
Crystal structure generator module.

This module contains the main function for generating crystal structures
using the Atomic Simulation Environment (ASE).
"""

import logging
from typing import Dict, Tuple, Optional
import numpy as np
from ase.build import bulk

from .constants import ELEMENTS, DEFAULT_SUPERCELL_SIZE
from .validators import validate_input, validate_structure

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_structure(
    element: str,
    structure_type: str,
    lattice_constant: Optional[float] = None,
    size: Tuple[int, int, int] = DEFAULT_SUPERCELL_SIZE,
    c_over_a: Optional[float] = None
) -> Dict:
    """
    Generate a crystal structure using ASE.
    
    Args:
        element (str): Chemical symbol (e.g., 'Cu' for Copper)
        structure_type (str): Crystal structure type ('fcc', 'bcc', 'hcp')
        lattice_constant (float, optional): Lattice constant in Å. If None, uses default for element
        size (tuple, optional): Supercell size as (nx, ny, nz). Defaults to (2, 2, 2)
        c_over_a (float, optional): c/a ratio for HCP structures. If None, uses default for element
    
    Returns:
        dict: JSON-compatible dictionary containing structure data with fields:
            - positions: List of atomic positions [x, y, z]
            - numbers: List of atomic numbers
            - cell: 3x3 matrix defining the unit cell
            - pbc: Periodic boundary conditions
            - metadata: Structure information
    
    Raises:
        ValueError: If input parameters are invalid
        TypeError: If input parameters are of wrong type
    """
    # Normalize structure type early
    structure_type = structure_type.lower()
    
    # Get element properties
    element_props = ELEMENTS[element]
    
    # Use default lattice constant if not provided
    if lattice_constant is None:
        lattice_constant = element_props.lattice_constants.get(structure_type)
        if lattice_constant is None:
            raise ValueError(f"No default lattice constant for {element} {structure_type}. Please provide one.")
    
    # Use default c/a ratio for HCP if not provided
    if structure_type == 'hcp' and c_over_a is None:
        if element_props.hcp_parameters is not None:
            c_over_a = element_props.hcp_parameters.get('c_over_a')
    
    # Validate input parameters
    validate_input(element, structure_type, lattice_constant, size, c_over_a)
    
    try:
        # Generate the base structure with correct parameters for each type
        if structure_type == 'hcp':
            if c_over_a is None:
                raise ValueError("c/a ratio is required for HCP structures")
            # For HCP, we need to set both a and c parameters
            c = float(lattice_constant) * float(c_over_a)  # Explicit float conversion
            atoms = bulk(element, 'hcp', a=lattice_constant, c=c)
        elif structure_type == 'fcc':
            # FCC conventional cell
            atoms = bulk(element, 'fcc', a=lattice_constant, cubic=True)
        elif structure_type == 'bcc':
            # BCC conventional cell
            atoms = bulk(element, 'bcc', a=lattice_constant, cubic=True)
        else:
            raise ValueError(f"Unknown structure: {structure_type}")
        
        # Create supercell
        atoms = atoms.repeat(size)
        
        # Validate the generated structure
        validate_structure(atoms)
        
        # Convert to JSON-compatible format
        structure_data = {
            "positions": atoms.get_positions().tolist(),
            "numbers": atoms.get_atomic_numbers().tolist(),
            "cell": atoms.get_cell().tolist(),
            "pbc": atoms.get_pbc().tolist(),
            "metadata": {
                "element": element,
                "structure_type": structure_type,
                "lattice_constant": lattice_constant,
                "c_over_a": c_over_a if structure_type == 'hcp' else None,
                "num_atoms": len(atoms),
                "supercell_size": size
            }
        }
        
        return structure_data
    except Exception as e:
        logger.error(f"Failed to generate structure: {str(e)}")
        raise 