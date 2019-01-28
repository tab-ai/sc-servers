#!/bin/bash

old_app_folder=$1
new_app_folder=$2

# parameter check
if [ ! 2 -eq $# ]; then
    echo "error (need 2 parameter)"
    exit 0
fi

# old_app_folder check
if [ ! -d $old_app_folder ]; then
    echo "$old_app_folder is not exists"
    exit 0
fi

# new_app_folder check
if [ -d $new_app_folder ]; then
    echo "$new_app_folder already is exists."
    exit 0
fi


sed -i "s/$old_app_folder/$new_app_folder/g" sc_project/settings.py
sed -i "s/$old_app_folder/$new_app_folder/g" $old_app_folder/apps.py
sed -i "s/$old_app_folder/$new_app_folder/g" run.sh
sed -i "s/$old_app_folder/$new_app_folder/g" sc_project/urls.py
sed -i "s/$old_app_folder/$new_app_folder/g" $old_app_folder/urls.py

mv $old_app_folder $new_app_folder
