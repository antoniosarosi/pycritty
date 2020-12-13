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

if [ -d "$base_path/pycritty" ]; then
    warn "Pycritty is already installed, skipping..."
else
    message "Cloning repository..."
    git clone https://github.com/antoniosarosi/pycritty $base_path/pycritty
fi

if [ -d $base_path/themes ]; then
    warn "Themes directory already exists, skipping..."
else
    message "Creating themes directory..."
    cp -r $base_path/pycritty/config/themes $base_path/themes
fi

if [ -f $base_path/fonts.yaml ]; then
    warn "fonts.yaml already exists, skipping..."
else
    message "Creating fonts file..."
    cp $base_path/pycritty/config/fonts.yaml $base_path/fonts.yaml
fi

bin_dir=~/.local/bin
if [ ! -d $bin_dir ]; then
    warn "~/.local/bin does not exists, creating directory..."
    mkdir -p $bin_dir
fi

if [ -f $bin_dir/pycritty ]; then
    warn "Executable already exists, skipping..."
else
    message "Creating executable..."
    ln -s $base_path/pycritty/src/main.py $bin_dir/pycritty
    chmod 755 $base_path/pycritty/src/main.py
fi

if ! echo $PATH | grep $bin_dir &> /dev/null; then
    warn '~/.local/bin not in $PATH, it will be added to your ~/.bashrc'
    echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
fi

message "\nPycritty installed successfully. Open a new terminal to test it!"

if [[ $1 != 'fonts' ]]; then
    exit 0
fi

if ! program_exists "curl"; then
    error "Fonts could not be installed, curl command not available"
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
tmp_file=pycritty_nerd_fonts_tmp.zip
for font in ${fonts[@]}; do
    curl -L "$font" -o $fonts_dir/$tmp_file
    unzip $fonts_dir/$tmp_file -d $fonts_dir
done

rm $fonts_dir/$tmp_file

message "\nFonts installed successfully!"
