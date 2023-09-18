#!/usr/bin/python3

from collections import defaultdict
import sys
import os
import hashlib


if len(sys.argv) != 3:
    print("not valid arguments, requires INF_FILE INI_FILE")
    sys.exit(1)

# read the INF file into lines
with open(sys.argv[1]) as f:
    content = f.read().split("\n")

data = defaultdict(defaultdict)
sect = None

for line in content:
    if not line:
        continue
    if line.startswith("[") and line.endswith("]"):
        sect = line[1 : len(line) - 1]
        continue
    if not sect:
        continue
    try:
        key, value = line.split("=")
        key = key.strip()
        value = value.strip()
    except ValueError:
        key = "Value"
        value = line.strip()
    if key in data[sect]:
        data[sect][key] += "," + value
    else:
        data[sect][key] = value

# extract .inf data and add to the .ini file
ini_data = {}
if "Defines" in data:
    defines = data["Defines"]
    if "FILE_GUID" in defines:
        ini_data["tag-id"] = defines["FILE_GUID"].lower()
    if "BASE_NAME" in defines:
        ini_data["software-name"] = defines["BASE_NAME"]
    if "VERSION_STRING" in defines:
        ini_data["version-scheme"] = "multipartnumeric"
        ini_data["software-version"] = defines["VERSION_STRING"]

# work out a SHA1 hash of all the files that made up the object file
if "Sources" in data:
    sources = data["Sources"]["Value"]
    m = hashlib.sha1()
    for source in sources.split(","):
        path = os.environ.get("SRCDIR", ".")
        with open(os.path.join(path, source), "rb") as f:
            m.update(f.read())
    ini_data["colloquial-version"] = m.hexdigest()

# this is the hash of the git tree
if "TREEHASH" in os.environ:
    ini_data["edition"] = os.environ["TREEHASH"]

with open(sys.argv[2], "wb") as f:
    f.write("[uSWID]\n".encode())
    for key, value in ini_data.items():
        f.write(f"{key}={value}\n".encode())

    # add deps: TODO: filter this to important ones?
    if "LibraryClasses" in data:
        for dep in data["LibraryClasses"]["Value"].split(","):
            f.write(f"[uSWID-Link:{dep}]\n".encode())
            f.write("rel=see-also\n".encode())
            f.write(f"href=swid:{dep}\n".encode())
