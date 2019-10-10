#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import os
import shutil


def unzip_archive(abs_name, format, path):
    res_filename = f"{abs_name}.{format}"
    res_filename = os.path.join(path, res_filename)
    with open(res_filename, 'wb') as file:
        i = 0
        while True:
            tmp_name = "{}_{:03}.{}".format(abs_name, i, format)
            tmp_abs_name = os.path.join(path, tmp_name)
            try:
                tmp_file = open(tmp_abs_name, 'rb')
                tmp_data = tmp_file.read()
                file.write(tmp_data)
                tmp_file.close()
                i += 1
            except FileNotFoundError:
                break

    result_path = os.path.join(path, abs_name)
    shutil.unpack_archive(res_filename, format=format, extract_dir=result_path)
    os.remove(res_filename)


if __name__ == "__main__":
    unzip_archive('english', 'zip', '/files/univer/english_zip_files')
