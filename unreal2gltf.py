import sys, getopt
import unreal

# Constants
GAME_PATH_ROOT = '/Game/' # Unreal needs this to find the content folder
SCRIPT_USAGE= """
Usage: unreal2gltf.py -i <input path> -o <output path > [flags]
    -i, --ipath=: Relative path to assets from the content directory. Ex. /path/to/input/
    -o, --opath=: Where the exported files will be sent. Has to be a full path. Ex. \'C:/path/to/output/\'
    -r, --recursive: Export assets from subdirectories. Will not preserve directory structure.
    -b, --binary: Will export assets in the '.glb' instead of the '.gltf' format.
    -d, --subdirs=: List of subdirectories to export separated by commas. Ex. path1,path2,path3
"""
VERSION_INFO= "unreal2gltf.py Version 1.0"

# Actual Export Function
def do_export(asset_directory: str, output_root: str, as_bin:bool, recurse:bool):
    # Check if input amd output were full directories
    if asset_directory[-1] == '/':
        asset_path = GAME_PATH_ROOT+asset_directory
    else:
        asset_path = GAME_PATH_ROOT+asset_directory+'/'
    
    # Import assets from given path and check if empty
    static_mesh_path = unreal.EditorAssetLibrary.list_assets(asset_path, recursive=recurse)
    number_of_assets = len(static_mesh_path)
    if number_of_assets == 0:
        unreal.log_error('unreal2gltf.py: No meshes found at '+asset_path)
        sys.exit()
    
    # Assign asset export options
    gltf_file_type = '.glb' if as_bin else '.gltf'
    export_options = unreal.GLTFExportOptions()
    export_options.bake_material_inputs = unreal.GLTFMaterialBakeMode.USE_MESH_DATA
    selected_actors = set()

    # Create export progress dialog and start export
    with unreal.ScopedSlowTask(number_of_assets, "Exporting Assets") as slow_task:
        slow_task.make_dialog(True)
        for asset in static_mesh_path:
            if slow_task.should_cancel():
                break
            slow_task.enter_progress_frame(1)

            static_mesh = unreal.EditorAssetLibrary.load_asset(asset)
            if unreal.MathLibrary.class_is_child_of(static_mesh.get_class(), unreal.StaticMesh.static_class()):
                # Creating export path by concatenating the output root, mesh name and file type
                # Also splicing the asset_path variable to account for /Game/
                # Also accounting for if the exports aren't binary make a folder for each asset
                if gltf_file_type == '.glb':
                    exportPath = output_root+asset_path[7:]+static_mesh.get_name()+gltf_file_type
                else:
                    exportPath = output_root+asset_path[7:]+static_mesh.get_name()+'/'+static_mesh.get_name()+gltf_file_type
                unreal.GLTFExporter.export_to_gltf(static_mesh,exportPath,export_options,selected_actors) # type: ignore

# Main Script Entry
def main(argv):
    # Program Variables
    input_directory = ''
    output_directory = ''
    subdirs = []
    using_subdirs = False
    recursive_flag = False
    as_binary = False
    
    # Define and check the commandline arguments
    try:
        opts, arg = getopt.getopt(argv,"bhi:o:r",["help","ipath=","opath=","recursive", "binary"])
    except getopt.GetoptError:
        unreal.log_error("unreal2gltf.py: Invalid Arguments. Try \'unreal2gltf.py -h\' for more information.")
        sys.exit(2)
    
    # Process arguments
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(SCRIPT_USAGE)
            sys.exit()
        elif opt in ("-i", "--ipath"):
            input_directory = arg
        elif opt in ("-o", "--opath"):
            output_directory = arg
        elif opt in ("-r","--recursive"):
            recursive_flag = True
        elif opt in ("-b", "--binary"):
            as_binary = True
        elif opt in ("-d", "--subdirs"):
            subdirs = arg.split(',')
            using_subdirs = True
    
    # Handle empty input path
    if input_directory == '':
        unreal.log_error('unreal2gltf.py: No input path provided! Try \'unreal2gltf.py -h\' for more information.')
        sys.exit()
    # Handle empty output path
    if output_directory == '':
        unreal.log_error('unreal2gltf.py: No output path provided! Try \'unreal2gltf.py -h\' for more information.')
        sys.exit()
    
    # Iterate through all subdirectory inputs if any
    if using_subdirs:
        for subdir in subdirs:
            if input_directory[-1] == '/':
                do_export(input_directory+subdir,output_directory,as_binary,recursive_flag)
            else:
                do_export(input_directory+'/'+subdir,output_directory,as_binary,recursive_flag)
    else:
        do_export(input_directory,output_directory,as_binary,recursive_flag)

# Run script if called from the commandline
if __name__ == "__main__":
    main(sys.argv[1:])
