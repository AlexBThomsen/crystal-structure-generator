"""
Common crystal structures generator.

This module provides functionality for generating a set of common crystal structures
and saving them to JSON files.
"""

import json
import logging
from pathlib import Path
from typing import Union, Optional

from .constants import ELEMENTS, DEFAULT_SUPERCELL_SIZE, ElementProperties
from .generator import generate_structure

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define representative elements for each structure type
REPRESENTATIVE_STRUCTURES = {
    'fcc': 'Cu',  # Copper as representative FCC
    'bcc': 'Fe',  # Iron as representative BCC
    'hcp': 'Ti'   # Titanium as representative HCP
}

def get_c_over_a(element_props: ElementProperties) -> Optional[float]:
    """Helper function to safely get c/a ratio from element properties."""
    if element_props.hcp_parameters is None:
        return None
    return element_props.hcp_parameters.get('c_over_a')

def generate_common_structures(output_dir: Union[str, Path] = ".") -> None:
    """
    Generate common crystal structures and save them as JSON files.
    
    This function generates a set of predefined crystal structures:
    - FCC Copper (Cu): Perfect example of face-centered cubic
    - BCC Iron (Fe): Classic body-centered cubic
    - HCP Titanium (Ti): Typical hexagonal close-packed
    Each structure is generated with default parameters and saved as a JSON file.
    
    Args:
        output_dir (str or Path): Directory to save the structure files. Defaults to current directory.
    """
    # Convert string path to Path object
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate structures based on representative elements
    structures = [
        {
            "element": element,
            "structure_type": struct_type,
            "size": DEFAULT_SUPERCELL_SIZE,
            # Use default lattice constant from ELEMENTS
            "lattice_constant": ELEMENTS[element].lattice_constants[struct_type],
            # Add c/a ratio for HCP structures
            "c_over_a": get_c_over_a(ELEMENTS[element]) if struct_type == 'hcp' else None
        }
        for struct_type, element in REPRESENTATIVE_STRUCTURES.items()
        if struct_type in ELEMENTS[element].supported_structures
    ]
    
    # Generate and save each structure
    for structure in structures:
        try:
            # Generate the structure using parameters from ELEMENTS
            data = generate_structure(**structure)
            
            # Create filename based on structure type
            filename = f"structure_{structure['structure_type']}.json"
            filepath = output_dir / filename
            
            # Save to JSON file
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Generated {filename}")
            logger.info(f"Element: {structure['element']}, "
                      f"Structure: {structure['structure_type']}, "
                      f"Lattice constant: {structure['lattice_constant']:.3f} Å")
            
            # Print stringified JSON for direct use
            logger.info(f"\nStringified JSON for {structure['structure_type']}:")
            print(json.dumps(data))
            
        except Exception as e:
            logger.error(f"Failed to generate {structure['structure_type']}: {str(e)}")

if __name__ == "__main__":
    try:
        # Generate common structures
        generate_common_structures()
        
        # Example of generating a custom structure
        logger.info("\nGenerating custom structure...")
        custom_structure = generate_structure(
            element="Cu",
            structure_type="fcc",
            size=(3, 3, 3)  # Larger supercell
        )
        print(json.dumps(custom_structure, indent=2))
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise 