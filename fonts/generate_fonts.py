#!/usr/bin/env python3
import fontforge
import os

def create_iberian_font(style_name, font_name, family_name, glyph_dir):
    print(f"========================================")
    print(f"Initializing: {font_name}")
    print(f"========================================")
    
    # Create a brand new font structure
    font = fontforge.font()
    font.fontname = font_name
    font.fullname = font_name
    font.familyname = family_name
    font.weight = "Regular"
    
    # Standard OS/2 typography metrics (1000 EM grid scale)
    font.ascent = 800
    font.descent = 200
    font.em = 1000
    
    # Complete target Palaeohispanic block matching our IME tables
    unicode_range = range(0x10200, 0x10240)
    
    # Create structural character slots
    for codepoint in unicode_range:
        hex_str = f"uni{codepoint:04X}"
        glyph = font.createChar(codepoint, hex_str)
        glyph.width = 600 # Default character layout width
        
        # Check if an SVG asset exists for this specific character slot
        svg_filename = f"{hex_str}.svg"
        svg_path = os.path.join(glyph_dir, svg_filename)
        
        if os.path.exists(svg_path):
            print(f" -> Importing vector asset for {hex_str} from {svg_path}")
            # Clear default contours and import the SVG outline path
            glyph.clear()
            glyph.importOutlines(svg_path)
            
            # Auto-align the drawn lines to fit nicely between baseline and cap-height
            glyph.autoTrace()
            glyph.correctDirection()
        else:
            # Fallback helper line: draw a light placeholder boundary if vector asset is missing
            pen = glyph.openPen()
            pen.moveTo(50, 0)
            pen.lineTo(550, 0)
            pen.lineTo(550, 700)
            pen.lineTo(50, 700)
            pen.closePath()
            print(f" !! Warning: Asset {svg_filename} missing. Created placeholder wireframe box.")

    # Generate standard space glyph required for digital typing
    space = font.createChar(32, "space")
    space.width = 300
    
    # Ensure build output folder exists
    os.makedirs("dist", exist_ok=True)
    
    # Output FontForge project native file
    font.save(f"dist/{font_name}.sfd")
    
    # Compile final scalable binary asset
    ttf_path = f"dist/{font_name}.ttf"
    font.generate(ttf_path)
    print(f"\nSuccessfully compiled: {ttf_path}")
    font.close()

if __name__ == "__main__":
    # Link each font compiler run to its corresponding vector asset subfolder
    create_iberian_font("Western", "IberianSemisyllabic-Western", "Iberian Semisyllabic", "src/western_glyphs")
    create_iberian_font("Eastern", "IberianSemisyllabic-Eastern", "Iberian Semisyllabic", "src/eastern_glyphs")
