#!/bin/bash

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
    if ! command -v $1 &> /dev/null; then
        error "Program $1 is not installed"
    fi
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
    mkdir $base_path
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
    mv $base_path/pycritty/themes $base_path
fi

if [ -f $base_path/fonts.yaml ]; then
    warn "fonts.yaml already exists, skipping..."
else
    message "Creating fonts file..."
    mv $base_path/pycritty/fonts.yaml $base_path
fi

bin_dir=~/.local/bin
if [ ! -d $bin_dir ]; then
    mkdir $bin_dir
fi

if [ -f $bin_dir/pycritty ]; then
    warn "Executable already exists, skipping..."
else
    message "Creating executable..."
    ln -s $base_path/pycritty/src/main.py $bin_dir/pycritty
fi

if [[ ! $bin_dir == *"$PATH"* ]]; then
    warn '~/.local/bin not in $PATH, it will be added'
    echo -e "\nexport PATH=$PATH:$bin_dir" >> ~/.bash_profile
fi

message "DONE! Open a new terminal to start using pycritty"

if [[ $1 == '-f' ]]; then
    message "Installing fonts..."
fi
