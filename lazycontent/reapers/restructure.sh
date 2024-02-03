#!/bin/bash

# Check if there are any arguments provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <subdirectory1> <subdirectory2> ..."
    exit 1
fi

# Iterate over the provided subdirectories and do something with each one
for subdir in "$@"; do
    if [ -d "$subdir" ]; then
        echo "Processing directory: $subdir"
	pushd "$subdir" > /dev/null
	
	mkdir "$subdir"
	mv * "$subdir"
	
	cp ../../lazycommon/pyproject.toml ../../lazycommon/.gitignore .
	sed -i "s/lazycommon/$subdir/g" "pyproject.toml"
	
	popd > /dev/null
        echo "Done with: $subdir"
    else
        echo "Directory not found: $subdir"
    fi
done

