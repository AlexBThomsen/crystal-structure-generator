"""
Example usage of the crystal structure generator.

This script demonstrates how to:
1. Generate common structures (Cu-FCC, Fe-BCC, Ti-HCP)
2. Create custom structures with different parameters
3. Create larger supercells
"""

from pathlib import Path
from crystal_structures import generate_structure, generate_common_structures

def main():
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    print("1. Generating common structures...")
    print("-" * 50)
    # This will create structure_fcc.json, structure_bcc.json, and structure_hcp.json
    generate_common_structures(output_dir)
    
    print("\n2. Generating custom structures...")
    print("-" * 50)
    
    # Example 1: Large copper FCC structure (3x3x3)
    print("\nGenerating 3x3x3 Copper FCC structure...")
    cu_large = generate_structure(
        element="Cu",
        structure_type="fcc",
        size=(3, 3, 3)  # This will create 108 atoms (4 atoms/cell × 3³)
    )
    
    # Example 2: Iron BCC with custom lattice parameter
    print("\nGenerating Iron BCC with custom lattice parameter...")
    fe_custom = generate_structure(
        element="Fe",
        structure_type="bcc",
        lattice_constant=2.90,  # Slightly larger than default
        size=(2, 2, 2)
    )
    
    # Example 3: Titanium HCP with custom c/a ratio
    print("\nGenerating Titanium HCP with custom c/a ratio...")
    ti_custom = generate_structure(
        element="Ti",
        structure_type="hcp",
        c_over_a=1.600,  # Custom c/a ratio
        size=(2, 2, 2)
    )
    
    # Example 4: Non-cubic supercell
    print("\nGenerating non-cubic Copper FCC supercell...")
    cu_noncubic = generate_structure(
        element="Cu",
        structure_type="fcc",
        size=(3, 2, 1)  # Different size in each direction
    )
    
    # Save custom structures
    custom_structures = {
        "cu_large_fcc.json": cu_large,
        "fe_custom_bcc.json": fe_custom,
        "ti_custom_hcp.json": ti_custom,
        "cu_noncubic_fcc.json": cu_noncubic
    }
    
    import json
    for filename, structure in custom_structures.items():
        filepath = output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(structure, f, indent=2)
        print(f"\nSaved {filename}")
        print(f"Number of atoms: {structure['metadata']['num_atoms']}")
        print(f"Structure type: {structure['metadata']['structure_type']}")
        print(f"Lattice constant: {structure['metadata']['lattice_constant']:.3f} Å")
        if structure['metadata']['c_over_a']:
            print(f"c/a ratio: {structure['metadata']['c_over_a']:.3f}")

if __name__ == "__main__":
    main() 