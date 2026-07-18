#!/usr/bin/env python3
import fontforge
import os
import json

def create_iberian_font(style_name, font_name, family_name):
    print(f"Initializing {font_name}...")
    
    # Create a brand new font object
    font = fontforge.font()
    font.fontname = font_name
    font.fullname = font_name
    font.familyname = family_name
    font.weight = "Regular"
    
    # Define standard OS/2 typography metrics
    font.ascent = 800
    font.descent = 200
    font.em = 1000
    
    # Base glyph checklist from our IME design
    unicode_range = range(0x10200, 0x10240)
    
    # Initialize character slots with clean default properties
    for codepoint in unicode_range:
        glyph = font.createChar(codepoint)
        glyph.glyphname = f"uni{codepoint:04X}"
        # Set a default advance width (how much space a character occupies horizontally)
        glyph.width = 600 

    # Ensure basic space character exists for text layouts
    space = font.createChar(32, "space")
    space.width = 300
    
    # Output directory handling
    os.makedirs("dist", exist_ok=True)
    
    # Save FontForge native SFD layout (useful for manual edits)
    sfd_path = f"dist/{font_name}.sfd"
    font.save(sfd_path)
    
    # Compile the ready-to-use TrueType binary file
    ttf_path = f"dist/{font_name}.ttf"
    font.generate(ttf_path)
    print(f"Successfully compiled: {ttf_path}")
    font.close()

if __name__ == "__main__":
    # Build both font variants cleanly in one execution pass
    create_iberian_font("Western", "IberianSemisyllabic-Western", "Iberian Semisyllabic")
    create_iberian_font("Eastern", "IberianSemisyllabic-Eastern", "Iberian Semisyllabic")
