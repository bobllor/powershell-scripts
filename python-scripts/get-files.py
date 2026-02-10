from pathlib import Path
from typing import TypedDict
import tempfile as tf
import argparse as ap
import os
import shutil
import uuid

# NOTE: these are not the exact arg types but the parsed data afterwards
class ArgData(TypedDict):
    source: Path
    output: str
    folders: list[str]
    ignore_files: list[str]
    match: bool

def get_uuid(uuid_max_len: int = 7) -> str:
    '''Returns a randomly generated UUID4.'''
    string: str = uuid.uuid4().hex

    if uuid_max_len > len(string):
        return string
    
    return string[:uuid_max_len]

def get_children(src: Path | str, *, include_dir: bool = False) -> list[Path]:
    '''Gets all children from a source folder recursively.'''
    src = Path(src)
    out: list[Path] = []

    for child in src.iterdir():
        if not child.is_dir():
            out.append(child.absolute())
        else:
            if include_dir:
                out.append(child.absolute())

            temp_children: list[Path] = get_children(child, include_dir=include_dir)

            out.extend(temp_children.copy())
    
    return out

def get_folder(src: Path | str, folder_name: str, *, match: bool = False) -> Path | None:
    '''Recusively searches for the folder name in a source folder.
    It returns the first folder found. It is case insensitive.

    If the folder cannot be found, then it will return None.

    Parameters
    ----------
        src: Path |str
            The source folder to search in.
        
        folder_name: str
            The target folder to search for.
        
        match: bool
            If true, then return the matching folder that contains the given folder name.
            By default this is false, always looking for the exact match.
    '''
    src = Path(src)
    folder_name: str = folder_name.lower()
    path: Path | None = None

    if folder_name.strip() == "":
        return path

    for child in src.iterdir():
        if child.is_dir():
            if child.name.lower() == folder_name:
                return child
            elif match and folder_name in child.name.lower():
                return child
            else:
                path = get_folder(child, folder_name, match=match)

                if path is not None:
                    return path

    return path 

def start_flatten(arg_data: ArgData) -> tuple[bool, str]:
    '''Starts the copy of files with a flattened output.
    
    It returns a tuple of a boolean status, and an error string if applicable.
    '''
    files: list[Path] = []
    missing_folders: list[str] = []

    for folder in arg_data["folders"]:
        folder_path: Path | None = get_folder(arg_data["source"], folder, match=arg_data["match"])
    
        if folder_path is not None:
            children: list[Path] = get_children(folder_path)

            files.extend(children.copy())
        else:
            print(f"Unable to find '{folder}' in '{arg_data["source"]}'")
            missing_folders.append(folder + "/")
    
    if len(missing_folders) > 0:
        return False, f"Unable to find folders: {" ".join(missing_folders)}"

    # used as a set to consume a matching argument if one is found
    ignore_files: set[str] = {file.lower() for file in arg_data["ignore_files"]}
    temp_files: list[str] = []
    for file in files:
        file_name: str = file.name.lower()
        
        if file_name in ignore_files:
            ignore_files.remove(file_name)
            print(f"Skipping file {file_name}, found in ignore")
            continue
    
        temp_files.append(file)
    
    files = temp_files

    if len(files) > 0:
        delete: bool = False
        parent_tmp_dir: Path = None
        with tf.TemporaryDirectory(delete=delete) as tmpdir:
            parent_tmp_dir = Path(tmpdir) 
            
        for file in files:
            shutil.copy(file, parent_tmp_dir / file.name)
        
        output_path: Path = Path(arg_data["output"]) 
        if output_path.exists():
            output_path = output_path.parent / (arg_data["output"] + get_uuid())

        os.replace(parent_tmp_dir, output_path)

        return True, f"Output generated: {output_path.absolute()}"
    else:
        return True, "No files found"


def start_keep(arg_data: ArgData) -> tuple[bool, str]:
    '''Starts the copy of files with the original structure kept in the output.
    
    It returns a tuple of a boolean status, and an error string if applicable.
    '''
    folders: list[Path] = []
    missing_folders: list[str] = []

    for folder in arg_data["folders"]:
        folder_path: Path | None = get_folder(arg_data["source"], folder, match=arg_data["match"])

        if folder_path is not None:
            folders.append(folder_path)
        else:
            print(f"Unable to find '{folder}' in '{arg_data["source"]}'")
            missing_folders.append(folder + "/")
    
    if len(missing_folders) > 0:
        return False, f"Unable to find folders: {" ".join(missing_folders)}"

    if len(folders) > 0:
        delete: bool = False
        tmp_dir_path: Path = None

        with tf.TemporaryDirectory(delete=delete) as tmpdir:
            tmp_dir_path = Path(tmpdir)

        for folder in folders:
            tmp_folder_path: Path = tmp_dir_path / folder.name
            tmp_folder_path.mkdir(exist_ok=True, parents=True)

            shutil.copytree(folder, tmp_folder_path, dirs_exist_ok=True)

        # removal of files from temp that are found as ignored
        files: list[Path] = get_children(tmp_dir_path)
        ignore_files: set[str] = {file.lower() for file in arg_data["ignore_files"]}
        for file in files:
            file_name: str = file.name.lower()
            if file_name in ignore_files:
                print(f"Removing file {file_name}, found in ignore")
                file.unlink(missing_ok=True)
                continue

        output_path: Path = Path(arg_data["output"]) 
        if output_path.exists():
            output_path = output_path.parent / (arg_data["output"] + get_uuid())

        os.replace(tmp_dir_path, output_path)

        return True, f"Output generated: {output_path.absolute()}"
    else:
        return True, "No folders found"


if __name__ == "__main__":
    parser: ap.ArgumentParser = ap.ArgumentParser(description="creates an output folder with files to prep for win32 app creation")

    # core arguments
    parser.add_argument("source", help="the source folder being searched in")
    parser.add_argument("-o", "--output", help="the output folder name", nargs=1, required=True)
    parser.add_argument("-f", "--folder", help="the target folder to copy files from", nargs="*", required=True)

    # optional
    parser.add_argument("-i", "--ignore", help="files to ignore from the target folder to copy to the output", nargs="*")
    parser.add_argument("-k", "--keep", help="keeps the structure of the target folder in the output", action="store_true")
    parser.add_argument("-m", "--match", help="enables substring matching for folder names", action="store_true")

    args: ap.Namespace = parser.parse_args()

    source: Path = Path(args.source)
    output: str = args.output[0]
    target_folders: list[str] = args.folder
    ignore_files: list[str] = [file.lower() for file in args.ignore or []]
    match: bool = args.match or False
    keep_structure: bool = args.keep or False

    arg_data: ArgData = {
        "folders": target_folders,
        "ignore_files": ignore_files,
        "match": match,
        "output": output,
        "source": source
    }

    # should probably add try-catch for the temp file creation? nah... should be fine.
    if not keep_structure:
        status, msg = start_flatten(arg_data)
    else:
        status, msg = start_keep(arg_data)

    print(msg)
    if not status:
        exit(1)