# unreal2gltf
A script for bulk exporting static meshes from Unreal Engine 5.0+ to the gltf or glb format.

## Setting up the Unreal Editor for Python scripting
The only prerequisite needed is to install and enable the Unreal Engine Editor Python Script Plguin. To do this you must go to **Edit->Plugins** and search for the **Python Editor Script Plugin**, enable it and restart your editor.

## Downloading and installing the script.
Download and extract the zip file from Github or clone the repository from the commandline. Take note of where you saved the script at.


## Project setup and usage from the Unreal Editor.
Ensure you have the Unreal Editor Python Script plugin enabled. Then:
1. **Edit->Project Settings...**
2. Once in your project look for **"Python"** under **"Plugins."**
3. Under **"Additional Paths"** add the path to the folder where you saved the script.
4. Restart your editor.

At the bottom of the Unreal Editor, there should be a text entry box next to "Cmd." Change **Cmd** to **Python** by clicking on it. Then enter the script as instructed in **Usage**.

## Usage

Usage: `unreal2gltf.py -i <input path> -o <output path> [additional flags] `

`-i`, `--ipath=`: Relative path to assets from the content directory. `Ex. /path/to/input/`

`-o`, `--opath=`: Where the exported files will be sent. Has to be a full path. `Ex. C:/path/to/output/`

`-r`, `--recursive`: Export assets from all subdirectories. Will not preserve directory structure of any folders not explictely chosen.

`-b`, `--binary`: Will export assets in the '.glb' instead of the '.gltf' format.

`-d`, `--subdirs=`: List of subdirectories to export separated by commas. This in attempt at preserving directory structure. `Ex. path1,path2,path3`

`-v`, `--version`: Get current version of the script and exit.

## Advanced Uage
This script can be run directly from the commandline. Unreal Documentation shows how to run Python scripts directly from the commandline [here](https://docs.unrealengine.com/5.0/en-US/scripting-the-unreal-editor-using-python/#thecommandline).
>[!WARNING]
> Running this script as a 'Commandlet' has been shown not to generate textures and materials for the assets exported.
