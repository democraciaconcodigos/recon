# -*- encoding: utf-8 -*-
#! /usr/bin/python

from subprocess import call
import os
import argparse
import distutils.core

def main():

    folder_path = parse_args()
    folder_name = os.path.dirname(folder_path)
    new_folder_path = "{0}-{1}".format(folder_name, "images")
    pdf_to_image(folder_path, new_folder_path)


def pdf_to_image(old_fp, new_fp):
    """pdf_to_image  
    Esta funcion transforma cada archivo .pdf de la carpeta old_fp en archivos
    .pbm en una nueva carpeta dada por el parametro new_fp. La jerarquia del
    directorio old_fp se respeta en el nuevo directorio, al igual que la
    ubicacion original de los archivos .pdf.
    
    This function converts each .pdf file in old_fp into .pbm files in a new 
    folder given by the new_fp parameter. The hierarchy of old_fp directory is 
    respected in the new directory, like the original location of the .pdf 
    files.
    
    """
    directory = os.listdir(old_fp)
    os.mkdir("{0}".format(new_fp))
    for elem in directory:
        elem_path = os.path.join(old_fp, elem)
        if os.path.isdir(elem_path):
            elem_path = os.path.join(old_fp, elem)
            new_elem_path = os.path.join(new_fp, elem)
            pdf_to_image(elem_path, new_elem_path)
        else:
            file_name, file_ext = os.path.splitext(elem)
            if (file_ext.find(".pdf") >= 0):
                file_path = os.path.join(old_fp, elem)
                new_file_path = os.path.join(new_fp, file_name)
                call(['pdfimages', file_path, new_file_path])


def parse_args():

    parser = argparse.ArgumentParser(
        description="Para ejecutar:\n\tpython pdf_to_image.py folder"
    )
    parser.add_argument("folder",
                        help="Carpeta donde se encuentran los archivos pdf",
                        type=str,
                        action="store"
                        )

    args = parser.parse_args()

    if os.path.isdir(args.folder):
        return args.folder
    else:
        print "La carpeta no existe !"
        exit(1)


if __name__ == "__main__":
    main()
