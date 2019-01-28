#/bin/bash

set -ue

script_dir=`dirname $0`

# bluetoothctl restart (STDERR)
echo "power off" | sudo bluetoothctl 1>/dev/null
echo "power on" | sudo bluetoothctl 1>/dev/null

# django makemigraions & migrate
$script_dir/manage.py makemigrations farm_01
$script_dir/manage.py migrate

# init superuser setting
cat $script_dir/init_user.py | $script_dir/manage.py shell

# sc-server start
$script_dir/manage.py runserver 0:80 --noreload
