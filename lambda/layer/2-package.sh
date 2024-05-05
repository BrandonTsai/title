#!/bin/bash -ex

if [ -f ./layer_content.zip]; then
 rm -rf layer_content.zip
fi

folder="./python"
if [ -d "$folder" ]; then
    echo "Folder '$folder' exists."
    # Clean up the contents in the folder
    rm -rf "$folder"/*
    echo "Contents in '$folder' cleaned up."
else
    echo "Folder '$folder' does not exist."
    # Create the folder
    mkdir "$folder"
    echo "Folder '$folder' created."
fi

cp -r create_layer/lib $folder/ && \
zip -r layer_content.zip $folder && \
rm -rf $folder/*