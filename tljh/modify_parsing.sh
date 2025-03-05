#!/bin/bash
# This script modifies the parsing.py file to fix a bug in pytorch_lightning and lightning

# 1. pytorch_lightning/utilities/parsing.py
# PL_PATH=$(pip show pytorch_lightning | awk '/Location:/ {print $2}')/pytorch_lightning
PL_PATH=/opt/tljh/user/lib/python3.10/site-packages/pytorch_lightning
TARGET_FILE="$PL_PATH/utilities/parsing.py"

if [ ! -f "$TARGET_FILE" ]; then
    echo "Error: File $TARGET_FILE not found!"
    exit 1
fi

# Modify line 102 using sed (in-place edit)
sed -i '102s/{k: local_vars\[k\] for k in init_parameters}/{k: local_vars[k] for k in init_parameters if k in local_vars}/' "$TARGET_FILE"
echo "Modification complete: $TARGET_FILE"

# 2. lightning/pytorch/utilities/parsing.py
# PL_PATH=$(pip show lightning | awk '/Location:/ {print $2}')/lightning
PL_PATH=/opt/tljh/user/lib/python3.10/site-packages/lightning
TARGET_FILE="$PL_PATH/pytorch/utilities/parsing.py"

if [ ! -f "$TARGET_FILE" ]; then
    echo "Error: File $TARGET_FILE not found!"
    exit 1
fi

# Modify line 102 using sed (in-place edit)
sed -i '102s/{k: local_vars\[k\] for k in init_parameters}/{k: local_vars[k] for k in init_parameters if k in local_vars}/' "$TARGET_FILE"
echo "Modification complete: $TARGET_FILE"
