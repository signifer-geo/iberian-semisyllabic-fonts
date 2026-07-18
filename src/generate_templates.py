#!/usr/bin/env python3
import os

def create_svg_template(filepath, codepoint):
    # Minimal SVG template (1000x1000 viewport)
    # Includes a light gray guide box for the baseline (y=800) and cap-height (y=100)
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="100%" height="100%">
  <!-- Typography guides (Will not be imported as glyph contours if left unjoined) -->
  <rect x="100" y="100" width="800" height="700" fill="none" stroke="#E0E0E0" stroke-width="2" stroke-dasharray="5,5" />
  <line x1="50" y1="800" x2="950" y2="800" stroke="#FF8080" stroke-width="2" stroke-dasharray="5,5" />
  
  <!-- DRAW YOUR IBERIAN CHARACTER STROKES BELOW HERE -->
  <!-- Example: Use <path d="..." fill="black"/> or clean vector lines -->
  
</svg>'''
    
    with open(filepath, 'w') as f:
        f.write(svg_content.strip())

def generate_all_templates():
    # Targets all hex files referenced by our compiler pipeline
    unicode_range = range(0x10200, 0x10240)
    directories = ["src/western_glyphs", "src/eastern_glyphs"]
    
    count = 0
    for d in directories:
        os.makedirs(d, exist_ok=True)
        for cp in unicode_range:
            filename = f"uni{cp:04X}.svg"
            filepath = os.path.join(d, filename)
            
            # Don't overwrite if you've already started drawing a file
            if not os.path.exists(filepath):
                create_svg_template(filepath, cp)
                count += 1
                
    print(f"Generated {count} new SVG glyph vector template frames.")

if __name__ == "__main__":
    generate_all_templates()
