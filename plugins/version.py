# Camera - Motion detecting camera with Telegram benefits
# Copyright (C) 2019-2021 SCP-079 <https://scp-079.org>
#
# This file is part of Camera.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from os import listdir, mkdir, remove
from os.path import exists, isfile, join
from shutil import move, rmtree


def delete_file(path: str) -> bool:
    # Delete a file
    result = False

    try:
        if not(path and exists(path)):
            return False

        result = remove(path) or True
    except Exception as e:
        print(f"Delete file error: {e}")

    return result


def move_file(src: str, dst: str) -> bool:
    # Move a file
    result = False

    try:
        if not src or not exists(src) or not dst:
            return False

        result = bool(move(src, dst))
    except Exception as e:
        print(f"Move file error: {e}")

    return result


def remove_dir(path: str) -> bool:
    # Remove a directory
    result = False

    try:
        if not path or not exists(path):
            return False

        result = rmtree(path) or True
    except Exception as e:
        print(f"Remove dir error: {e}")

    return result


def files(path):
    # List files, not directories
    for file in listdir(path):
        if isfile(join(path, file)):
            yield file


def version_0() -> bool:
    # Version 0
    result = False

    try:
        exists("data/tmp") and rmtree("data/tmp")

        for path in ["data", "data/config", "data/pickle", "data/pickle/backup",
                     "data/log", "data/session", "data/tmp"]:
            not exists(path) and mkdir(path)

        result = True
    except Exception as e:
        print(f"Version 0 error: {e}")

    return result


def version_control() -> bool:
    # Version control
    result = False

    try:
        version_0()

        result = True
    except Exception as e:
        print(f"Version control error: {e}")

    return result
