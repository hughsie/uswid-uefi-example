#!/usr/bin/python3

import sys
import hashlib


if len(sys.argv) < 3:
    print("not valid arguments, requires IN_FILE OUT_FILE BIN_FILE")
    sys.exit(1)

# read file
with open(sys.argv[1], "rb") as f:
    data = f.read().decode()

# replace @SHA256@
m = hashlib.sha256()
for fn in sys.argv[3:]:
    with open(fn, "rb") as f:
        m.update(f.read())
data = data.replace("@SHA256@", m.hexdigest())

# write file
with open(sys.argv[2], "wb") as f:
    f.write(data.encode())
