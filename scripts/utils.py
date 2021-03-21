import os


def get_files(path: str):
    return next(os.walk(path))[2]


def get_file(path: str, file_name: str):
    return os.path.join(path, file_name)
