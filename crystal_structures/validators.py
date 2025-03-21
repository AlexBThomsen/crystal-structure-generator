"""
Validation functions for crystal structure generation.

This module contains functions for validating input parameters and
generated structures to ensure they meet physical and logical constraints.
"""

from typing import Tuple, Optional
import numpy as np
from ase.atoms import Atoms
from ase.geometry import cell_to_cellpar

from .constants import ELEMENTS, VALID_STRUCTURES

def validate_input(
    element: str,
    structure_type: str,
    lattice_constant: float,
    size: Tuple[int, int, int],
    c_over_a: Optional[float] = None
) -> None:
    """
    Validate input parameters for structure generation.
    
    Args:
        element (str): Chemical symbol of the element
        structure_type (str): Type of crystal structure ('fcc', 'bcc', or 'hcp')
        lattice_constant (float): Lattice constant in Angstroms
        size (tuple): Supercell size as (nx, ny, nz)
        c_over_a (float, optional): c/a ratio for HCP structures
    
    Raises:
        TypeError: If parameters are of wrong type
        ValueError: If parameters have invalid values
    """
    # Type checking
    if not isinstance(element, str):
        raise TypeError(f"Element must be a string, got {type(element)}")
    if not isinstance(structure_type, str):
        raise TypeError(f"Structure type must be a string, got {type(structure_type)}")
    if not isinstance(lattice_constant, (int, float)):
        raise TypeError(f"Lattice constant must be a number, got {type(lattice_constant)}")
    if not isinstance(size, tuple) or len(size) != 3:
        raise TypeError("Size must be a 3-tuple of integers")
    if not all(isinstance(s, int) for s in size):
        raise TypeError("Size components must be integers")
    if c_over_a is not None and not isinstance(c_over_a, (int, float)):
        raise TypeError(f"c/a ratio must be a number, got {type(c_over_a)}")

    # Value validation
    if element not in ELEMENTS:
        raise ValueError(f"Unsupported element: {element}. Supported elements: {list(ELEMENTS.keys())}")
    
    structure_type = structure_type.lower()
    if structure_type not in VALID_STRUCTURES:
        raise ValueError(f"Invalid structure type: {structure_type}. Must be one of: {VALID_STRUCTURES}")
    
    # Check if structure type is supported for this element
    element_props = ELEMENTS[element]
    if structure_type not in element_props.supported_structures:
        raise ValueError(f"Structure type {structure_type} is not supported for element {element}")
    
    if lattice_constant <= 0:
        raise ValueError(f"Invalid lattice constant: {lattice_constant}. Must be positive")
    
    if any(s <= 0 for s in size):
        raise ValueError(f"Invalid supercell size: {size}. All dimensions must be positive")
    
    if structure_type == 'hcp':
        if c_over_a is None:
            if element_props.hcp_parameters is None:
                raise ValueError(f"No default c/a ratio for {element}. Please provide one.")
        elif c_over_a <= 0:
            raise ValueError("HCP structures require a positive c/a ratio")

def validate_structure(atoms: Atoms) -> None:
    """
    Validate the generated atomic structure.
    
    Args:
        atoms (Atoms): ASE Atoms object to validate
    
    Raises:
        ValueError: If the structure is invalid
    """
    # Check if all atoms are within the cell
    cell = atoms.get_cell()
    scaled_positions = atoms.get_scaled_positions()
    if not np.all((scaled_positions >= 0) & (scaled_positions <= 1)):
        raise ValueError("Some atoms are outside the unit cell")
    
    # Check cell parameters
    cellpar = cell_to_cellpar(cell)
    if np.any(cellpar[:3] <= 0):
        raise ValueError("Invalid cell parameters: some lengths are zero or negative")
    if np.any(np.abs(cellpar[3:]) > 180):
        raise ValueError("Invalid cell parameters: angles must be between 0 and 180 degrees")

    # Additional checks could be added here:
    # - Minimum distance between atoms
    # - Cell volume
    # - Symmetry operations 