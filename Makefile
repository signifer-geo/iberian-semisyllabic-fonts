# Project configurations
FONT_SCRIPT = fonts/generate_fonts.py
IME_DIR = ime
DIST_DIR = dist
FCITX5_LOCAL_DIR = ~/.local/share/fcitx5

.PHONY: all fonts ime clean install

all: fonts ime

# Step 1: Compile the TrueType fonts via FontForge
fonts:
	@echo "=== Compiling Iberian Fonts ==="
	python3 $(FONT_SCRIPT)

# Step 2: Compile Fcitx5 layout source files into binary dictionary modules
ime:
	@echo "=== Compiling Fcitx5 Table Binaries ==="
	@mkdir -p $(DIST_DIR)
	# Compile Western signary IME table
	libime_table_compiler $(IME_DIR)/iberian-western.txt $(DIST_DIR)/iberian-western.main.dict
	# Compile Eastern signary IME table
	libime_table_compiler $(IME_DIR)/iberian-eastern.txt $(DIST_DIR)/iberian-eastern.main.dict
	
	# Generate Fcitx5 addon configuration blueprints
	@echo "[InputMethod]\nName=iberian-western\nIcon=input-keyboard\nLabel=IbW\nLangCode=und\nTable=$(DIST_DIR)/iberian-western.main.dict\nPageSize=5" > $(DIST_DIR)/iberian-western.conf
	@echo "[InputMethod]\nName=iberian-eastern\nIcon=input-keyboard\nLabel=IbE\nLangCode=und\nTable=$(DIST_DIR)/iberian-eastern.main.dict\nPageSize=5" > $(DIST_DIR)/iberian-eastern.conf

# Step 3: Install everything locally into the Debian system configuration paths
install: all
	@echo "=== Installing Fonts and IME Layouts ==="
	# Install fonts to user local directory
	mkdir -p ~/.local/share/fonts/
	cp $(DIST_DIR)/*.ttf ~/.local/share/fonts/
	fc-cache -f -v
	
	# Install IME dictionaries and metadata configurations to Fcitx5 local targets
	mkdir -p $(FCITX5_LOCAL_DIR)/table
	mkdir -p $(FCITX5_LOCAL_DIR)/inputmethod
	cp $(DIST_DIR)/*.main.dict $(FCITX5_LOCAL_DIR)/table/
	cp $(DIST_DIR)/*.conf $(FCITX5_LOCAL_DIR)/inputmethod/
	@echo "Installation complete! Please restart Fcitx5 ('fcitx5 -r') to load changes."

# Clean built binaries
clean:
	rm -rf $(DIST_DIR)
	@echo "Build directory cleared."
