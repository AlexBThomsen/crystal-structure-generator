"""
Constants and configuration for crystal structure generation.

This module contains all the constant values and configurations needed for
generating crystal structures, including element properties and default parameters.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class ElementProperties:
    """Properties of a chemical element relevant for crystal structure generation."""
    atomic_number: int
    supported_structures: List[str]
    lattice_constants: Dict[str, float]
    hcp_parameters: Optional[Dict[str, float]] = None

# Comprehensive element properties including supported structures and parameters
ELEMENTS = {
    'Cu': ElementProperties(
        atomic_number=29,
        supported_structures=['fcc'],
        lattice_constants={'fcc': 3.61}  # Copper FCC
    ),
    'Fe': ElementProperties(
        atomic_number=26,
        supported_structures=['bcc'],
        lattice_constants={'bcc': 2.87}  # Iron BCC
    ),
    'Ti': ElementProperties(
        atomic_number=22,
        supported_structures=['hcp'],
        lattice_constants={'hcp': 2.95},  # Titanium HCP
        hcp_parameters={'c_over_a': 1.587}
    ),
    'Al': ElementProperties(
        atomic_number=13,
        supported_structures=['fcc'],
        lattice_constants={'fcc': 4.05}  # Aluminum FCC
    ),
    'Ni': ElementProperties(
        atomic_number=28,
        supported_structures=['fcc'],
        lattice_constants={'fcc': 3.52}  # Nickel FCC
    ),
    'Pt': ElementProperties(
        atomic_number=78,
        supported_structures=['fcc'],
        lattice_constants={'fcc': 3.92}  # Platinum FCC
    ),
    'Au': ElementProperties(
        atomic_number=79,
        supported_structures=['fcc'],
        lattice_constants={'fcc': 4.08}  # Gold FCC
    ),
    'Ag': ElementProperties(
        atomic_number=47,
        supported_structures=['fcc'],
        lattice_constants={'fcc': 4.09}  # Silver FCC
    ),
    'Zn': ElementProperties(
        atomic_number=30,
        supported_structures=['hcp'],
        lattice_constants={'hcp': 2.66},
        hcp_parameters={'c_over_a': 1.856}  # Zinc HCP
    ),
    'Mg': ElementProperties(
        atomic_number=12,
        supported_structures=['hcp'],
        lattice_constants={'hcp': 3.21},
        hcp_parameters={'c_over_a': 1.624}  # Magnesium HCP
    )
}

# Valid structure types
VALID_STRUCTURES = ['fcc', 'bcc', 'hcp']

# Default supercell size
DEFAULT_SUPERCELL_SIZE = (2, 2, 2)

# Logging format
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s' 