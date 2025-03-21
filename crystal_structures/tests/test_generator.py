"""
Tests for the crystal structure generator.

This module contains comprehensive tests for the structure generation functionality,
including validation of structure types, atom counts, and error handling.
"""

import pytest
import numpy as np
from pathlib import Path

from crystal_structures import (
    generate_structure,
    generate_common_structures,
    ELEMENTS,
    DEFAULT_SUPERCELL_SIZE
)
from crystal_structures.validators import validate_input

# Test fixtures
@pytest.fixture
def temp_output_dir(tmp_path):
    """Provide a temporary directory for output files."""
    return tmp_path

# Parametrized test data
STRUCTURE_PARAMS = [
    ('Cu', 'fcc', None, 32),  # 4 atoms/unit cell * 2^3
    ('Fe', 'bcc', None, 16),  # 2 atoms/unit cell * 2^3
    ('Ti', 'hcp', None, 16)   # 2 atoms/unit cell * 2^3
]

# Split invalid inputs into two categories: KeyError and ValueError
INVALID_ELEMENT = [
    ('XX', 'fcc', 3.61, (2, 2, 2), None)  # Should raise KeyError
]

INVALID_INPUTS = [
    ('Cu', 'invalid', 3.61, (2, 2, 2), None, "Invalid structure type"),
    ('Cu', 'fcc', -1.0, (2, 2, 2), None, "Invalid lattice constant"),
    ('Cu', 'fcc', 3.61, (-1, 2, 2), None, "Invalid supercell size"),
    ('Ti', 'hcp', 3.61, (2, 2, 2), -1.0, "HCP structures require a positive c/a ratio")
]

SUPERCELL_SIZES = [
    ((1, 1, 1), 4),   # FCC unit cell
    ((2, 2, 2), 32),  # 2x2x2 supercell
    ((3, 2, 1), 24)   # Non-cubic supercell
]

# Basic structure generation tests
@pytest.mark.parametrize("element,structure_type,lattice_const,expected_atoms", STRUCTURE_PARAMS)
def test_structure_generation(element, structure_type, lattice_const, expected_atoms):
    """Test generation of basic structure types with default parameters."""
    structure = generate_structure(
        element=element,
        structure_type=structure_type,
        lattice_constant=lattice_const,
        size=DEFAULT_SUPERCELL_SIZE
    )
    
    assert structure is not None
    assert len(structure['positions']) == expected_atoms
    assert len(structure['numbers']) == expected_atoms
    assert all(num == ELEMENTS[element].atomic_number for num in structure['numbers'])
    assert structure['metadata']['element'] == element
    assert structure['metadata']['structure_type'] == structure_type.lower()
    assert structure['metadata']['num_atoms'] == expected_atoms

# Test invalid element handling
@pytest.mark.parametrize("element,structure_type,lattice_const,size,c_over_a", INVALID_ELEMENT)
def test_invalid_element(element, structure_type, lattice_const, size, c_over_a):
    """Test handling of invalid elements."""
    with pytest.raises(KeyError):
        generate_structure(
            element=element,
            structure_type=structure_type,
            lattice_constant=lattice_const,
            size=size,
            c_over_a=c_over_a
        )

# Test error handling for other invalid inputs
@pytest.mark.parametrize(
    "element,structure_type,lattice_const,size,c_over_a,expected_error",
    INVALID_INPUTS
)
def test_invalid_inputs(element, structure_type, lattice_const, size, c_over_a, expected_error):
    """Test error handling for invalid inputs."""
    with pytest.raises(ValueError) as exc_info:
        generate_structure(
            element=element,
            structure_type=structure_type,
            lattice_constant=lattice_const,
            size=size,
            c_over_a=c_over_a
        )
    assert expected_error in str(exc_info.value)

# Test type checking
def test_type_validation():
    """Test type checking in validate_input function."""
    with pytest.raises(TypeError):
        validate_input(123, 'fcc', 3.61, (2, 2, 2))  # Invalid element type
    with pytest.raises(TypeError):
        validate_input('Cu', 'fcc', '3.61', (2, 2, 2))  # Invalid lattice constant type
    with pytest.raises(TypeError):
        validate_input('Cu', 'fcc', 3.61, [2, 2, 2])  # Invalid size type

# Test supercell generation
@pytest.mark.parametrize("size,expected_atoms", SUPERCELL_SIZES)
def test_supercell_sizes(size, expected_atoms):
    """Test various supercell sizes."""
    structure = generate_structure('Cu', 'fcc', size=size)
    assert structure['metadata']['num_atoms'] == expected_atoms
    assert structure['metadata']['supercell_size'] == size

# Test file generation
def test_generate_common_structures(temp_output_dir):
    """Test generation and saving of common structures."""
    generate_common_structures(temp_output_dir)
    
    # Check if files were created
    expected_files = ['structure_fcc.json', 'structure_bcc.json', 'structure_hcp.json']
    for filename in expected_files:
        assert (temp_output_dir / filename).exists()
        
    # Verify file contents
    for filename in expected_files:
        with open(temp_output_dir / filename, 'r') as f:
            data = pytest.importorskip("json").load(f)
            assert 'positions' in data
            assert 'numbers' in data
            assert 'cell' in data
            assert 'metadata' in data

# Test HCP specific features
def test_hcp_structure():
    """Test specific features of HCP structures."""
    structure = generate_structure(
        'Ti',
        'hcp',
        size=(1, 1, 1)
    )
    
    # Check c/a ratio
    cell = np.array(structure['cell'])
    c = np.linalg.norm(cell[2])
    a = np.linalg.norm(cell[0])
    assert abs(c/a - ELEMENTS['Ti'].hcp_parameters['c_over_a']) < 1e-10

# Test case sensitivity
def test_case_insensitivity():
    """Test that structure type is case-insensitive."""
    structure_lower = generate_structure('Cu', 'fcc', size=(1, 1, 1))
    structure_upper = generate_structure('Cu', 'FCC', size=(1, 1, 1))
    
    assert structure_lower['metadata']['structure_type'] == structure_upper['metadata']['structure_type']
    assert np.array_equal(structure_lower['positions'], structure_upper['positions'])

if __name__ == '__main__':
    pytest.main(['-v', __file__]) 