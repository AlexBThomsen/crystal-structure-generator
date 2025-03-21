"""
Crystal Structures Script

A script for generating common crystal structures using the Atomic Simulation Environment (ASE).
"""

from .generator import generate_structure
from .common_structures import generate_common_structures
from .constants import ELEMENTS, VALID_STRUCTURES, DEFAULT_SUPERCELL_SIZE

__all__ = [
    'generate_structure',
    'generate_common_structures',
    'ELEMENTS',
    'VALID_STRUCTURES',
    'DEFAULT_SUPERCELL_SIZE'
]

__version__ = '1.0.0' 