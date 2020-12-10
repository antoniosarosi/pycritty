#!/bin/bash

# Pycritty install script

RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
NORMAL="\033[0m"

warn() {
    echo -e "${YELLOW}$1${NORMAL}" >&2
}

error() {
    echo -e "${RED}$1${NORMAL}" >&2
    exit 1
}

message() {
    echo -e "${GREEN}$1${NORMAL}"
}

program_exists() {
    command -v $1 &> /dev/null
}

if ! program_exists "git"; then
    error "Git is not installed"
fi

if ! program_exists "alacritty"; then
    warn "WARNING: Alacritty is not installed"
fi

base_path=~/.config/alacritty

if [ ! -d $base_path ]; then
    warn "WARNING: Alacritty config directory not present, it will be created"
    mkdir -p $base_path
fi

if [ ! -f "$base_path/alacritty.yml" ]; then
    warn "WARNING: Alacritty config file not present, it will be created"
    touch $base_path/alacritty.yml
fi

message "Cloning repository..."
git clone https://github.com/antoniosarosi/pycritty $base_path/pycritty

if [ -d $base_path/themes ]; then
    warn "Themes directory already exists, skipping..."
else
    message "Creating themes directory..."
    ln -s $base_path/pycritty/themes $base_path/themes
fi

if [ -f $base_path/fonts.yaml ]; then
    warn "fonts.yaml already exists, skipping..."
else
    message "Creating fonts file..."
    ln -s $base_path/pycritty/fonts.yaml $base_path/fonts.yaml
fi

bin_dir=~/.local/bin
if [ ! -d $bin_dir ]; then
    mkdir -p $bin_dir
fi

if [ -f $bin_dir/pycritty ]; then
    warn "Executable already exists, skipping..."
else
    message "Creating executable..."
    ln -s $base_path/pycritty/src/main.py $bin_dir/pycritty
    chmod 755 $base_path/pycritty/src/main.py
fi

if ! echo $PATH | grep $bin_dir; then
    warn '~/.local/bin not in $PATH, it will be added'
    echo -e "\nexport PATH=$PATH:$bin_dir" >> ~/.bash_profile
fi

message "\nPycritty installed successfully. Open a new terminal to test it!"

echo "Install fonts? (default: No) [y/n]: "
read install_fonts

if [[ $install_fonts != [yY] ]]; then
    exit 0
fi

if ! program_exists "unzip"; then
    error "Fonts could not be installed, unzip command not available"
fi

fonts=(
    # Agave
    'https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/Agave.zip'
    # Caskaydia
    'https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/CascadiaCode.zip'
    # DaddyTimeMono
    'https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/DaddyTimeMono.zip'
    # Hack
    'https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/Hack.zip'
    # Hurmit
    'https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/Hermit.zip'
    # Iosevka
    'https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/Iosevka.zip'
    # JetBrains
    'https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/JetBrainsMono.zip'
    # Mononoki
    'https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/Mononoki.zip'
    # UbuntuMono
    'https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/UbuntuMono.zip'
    # SpaceMono
    'https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/SpaceMono.zip'
)

fonts_dir=~/.local/share/fonts
if [ ! -d $fonts_dir ]; then
    warn "Creating directory ~/.local/share/fonts"
    mkdir -p $fonts_dir
fi

message "Installing fonts..."
for font in ${fonts[@]}; do
    curl -L "$font" -o $fonts_dir/font.zip
    unzip $fonts_dir/font.zip -d $fonts_dir
done

rm $fonts_dir/font.zip

message "\nFonts installed successfully!"
