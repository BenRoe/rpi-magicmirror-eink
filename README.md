## Install dependencies

- Update packages and install Git, Chrome Browser
```shell
sudo apt-get update && sudo apt-get install -y git chromium-browser
```

## Setup
- Clone/copy the project files to your system.
```shell
git clone https://github.com/BenRoe/rpi-magicmirror-eink.git
```

- Move to the project folder
```shell
cd rpi-magicmirror-eink
```

- Install Node.js dependencies (inside the `rpi-magicmirror-eink` folder)
```shell
npm install
```

- Copy all files & folder from `magicmirror-files` to you MagicMirror css folder.  
*Example: copy all files from magicmirror-files folder to the MagicMirror/css folder in the home directory.*
```shell
cp -a magicmirror-files/. ~/MagicMirror/css/
```

- dfdf

## Ressources
- [Cherry bitmap font](https://github.com/turquoise-hexagon/cherry) by [marin](https://github.com/turquoise-hexagon) converted to ttf with [Bits'N'Picas](https://github.com/kreativekorp/bitsnpicas)
- The project uses the Original Library written by Waveshare. It can be downloaded [here](https://www.waveshare.com/wiki/Main_Page#OLEDs_.2F_LCDs).

## Licence
MIT. See LICENCE.md
