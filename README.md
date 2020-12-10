# Pycritty

Change your alacritty config on the fly!

![Preview](img/preview.png)

## Installation:

### Install Script

```bash
curl "https://raw.githubusercontent.com/antoniosarosi/pycritty/master/install.sh" | bash
```

### Manual Installation

```bash
mkdir -p ~/.config/alacritty
cd ~/.config/alacritty
git clone https://github.com/antoniosarosi/pycritty
ln -s pycritty/fonts.yaml fonts.yaml
ln -s pycritty/themes themes
ln -s pycritty/src/main.py ~/.local/bin/pycritty
chmod 755 pycritty/src/main.py
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bash_profile
```

## Usage:

```bash
pycritty --font UbuntuMono --size 14 --opacity 0.95
```
