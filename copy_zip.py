from shutil import copyfile
from cumulus_file_rename import __version__


if __name__ == "__main__":

    src = "/home/fileRename.zip"
    dest = "/home/zip_file/fileRename-" + __version__ + '.zip'
    copyfile(src, dest)
