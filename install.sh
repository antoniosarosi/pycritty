#!/bin/bash

# Pycritty install script

RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'

BOLD='\033[1m'
ITALIC='\033[3m'
NORMAL="\033[0m"

color_print() {
    if [ -t 1 ]; then
        echo -e "$@$NORMAL"
    else
        echo "$@" | sed "s/\\\033\[[0-9;]*m//g"
    fi
}

stderr_print() {
    color_print "$@" >&2
}

warn() {
    stderr_print "$YELLOW$1"
}

error() {
    stderr_print "$RED$1"
    exit 1
}

ok() {
    color_print "$GREEN$1"
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
    warn "Alacritty config directory not found"
    stderr_print "Creating dir =>" $BLUE$base_path
    mkdir -p $base_path
fi

if [ ! -f $base_path/alacritty.yml ]; then
    warn "Alacritty config file not found"
    stderr_print "Creating file =>" $BLUE$base_path/alacritty.yml
    touch $base_path/alacritty.yml
fi

if [ -d $base_path/pycritty ]; then
    warn "Pycritty is already installed, skipping..."
else
    repo="https://github.com/antoniosarosi/pycritty"
    color_print "Cloning repo =>" $CYAN$repo
    git clone -q $repo $base_path/pycritty
    if (( $? != 0 )); then
        error "Failed cloning repository, cannot install pycritty"
    fi
fi

if [ -d $base_path/themes ]; then
    warn "Themes directory already exists, skipping..."
else
    color_print "Creating themes dir =>" $BLUE$base_path/themes
    cp -r $base_path/pycritty/config/themes $base_path/themes
fi

if [ -f $base_path/fonts.yaml ]; then
    warn "fonts.yaml already exists, skipping..."
else
    color_print "Creating fonts file =>" $BLUE$base_path/fonts.yaml
    cp $base_path/pycritty/config/fonts.yaml $base_path/fonts.yaml
fi

bin_dir=~/.local/bin
if [ ! -d $bin_dir ]; then
    warn "Local bin directory not found"
    stderr_print "Creating dir =>" $BLUE$bin_dir
    mkdir -p $bin_dir
fi

if [ -f $bin_dir/pycritty ]; then
    warn "Executable already exists, skipping..."
else
    color_print "Creating executable =>" $BLUE$bin_dir/pycritty
    ln -s $base_path/pycritty/src/main.py $bin_dir/pycritty
    chmod 755 $base_path/pycritty/src/main.py
fi

if ! echo $PATH | grep $bin_dir &> /dev/null; then
    warn '~/.local/bin not in $PATH'
    new_path='export PATH="$PATH:$HOME/.local/bin"'
    stderr_print "Creating new path =>$PURPLE echo $new_path >> ~/.bashrc"
    echo $new_path >> ~/.bashrc
fi

ok "Pycritty installed successfully. Open a new terminal to test it!"

if [[ $1 != 'fonts' ]]; then
    exit 0
fi

if ! program_exists "curl"; then
    error "Fonts could not be installed, curl command not available"
fi

if ! program_exists "unzip"; then
    error "Fonts could not be installed, unzip command not available"
fi

declare -A fonts=(
    [Agave]='https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/Agave.zip'
    [Caskaydia]='https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/CascadiaCode.zip'
    [DaddyTimeMono]='https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/DaddyTimeMono.zip'
    [Hack]='https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/Hack.zip'
    [Hurmit]='https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/Hermit.zip'
    [Iosevka]='https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/Iosevka.zip'
    [JetBrains]='https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/JetBrainsMono.zip'
    [Mononoki]='https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/Mononoki.zip'
    [UbuntuMono]='https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/UbuntuMono.zip'
    [SpaceMono]='https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/SpaceMono.zip'
)

fonts_dir=~/.local/share/fonts
if [ ! -d $fonts_dir ]; then
    warn "Local fonts directory not found"
    stderr_print "Creating dir =>" $BLUE$fonts_dir
    mkdir -p $fonts_dir
fi

echo "Installing fonts..."
tmp_file=pycritty_nerd_fonts_tmp.zip
for font in ${!fonts[@]}; do
    link=${fonts[${font}]}
    color_print "Downloading =>" $CYAN$link
    curl -sL "$link" -o $fonts_dir/$tmp_file
    color_print "Installing font =>" $PURPLE$font
    unzip -qn $fonts_dir/$tmp_file -d $fonts_dir
done

rm $fonts_dir/$tmp_file

ok "Fonts installed successfully!"
