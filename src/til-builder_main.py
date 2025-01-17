import os
import pathlib
from utils.helper_functions import has_txt_extension, has_md_extension
from utils.commandline import cl_args
import version

from builder.html_builder import generate_html_for_file, generate_files

# Global variables
OUTPUT_PATH = cl_args.output

def main():
    """Entry point for the app"""

    # Check for exit commands (Return if any branch is entered)
    if cl_args.version:
        print(f"{version.__name__}: {version.__version__}")
        exit(0)

    # Execute parse functions
    input_path = cl_args.input_path
    if input_path is None:
        print("You need to specify a file or folder of text files that need to be converted!")
        exit(-1)

    # Check if the pathname is a directory
    if os.path.isdir(input_path):
        # Create a Path object for the directory
        directory = pathlib.Path(input_path)

        # Use the rglob() method to get a list of all files in the directory and its subdirectories
        files_in_directory = list(filter(lambda file_path: 
                                         os.path.isfile(file_path) and has_txt_extension(file_path) or has_md_extension(file_path), 
                                         list(map(lambda file_path: str(file_path.absolute()).replace('\\', '/'), 
                                                  list(directory.rglob('*'))))))

        files_to_be_generated = []

        for file in files_in_directory:
            files_to_be_generated.append(generate_html_for_file(file))

        generate_files(files_to_be_generated)

    elif os.path.isfile(input_path):
        # Check if a text file is supplied
        if has_txt_extension(input_path) or has_md_extension(input_path):
            generate_files([generate_html_for_file(input_path)])
        else:
            print(f"Only text and markdown files are supported. {input_path} is not a text or markdown file!")
            exit(-1)
    else:
        print(f"'{input_path}' does not exist or is neither a file nor a directory.")
        exit(-1)

    # Everything went well
    exit(0)


if __name__ == "__main__":
    main()
