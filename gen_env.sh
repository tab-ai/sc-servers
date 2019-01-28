#!/bin/bash

# [ -f .env ] && exit 0

cat>.env<<EOF
PGDB_PATH=/home/pgdb
PGDB_USER=root
PGDB_PASSWORD=1234567
PGDB_DB=sc
PGDB_HOST=localhost
PGDB_PORT=5433
EOF

ln -sf $(pwd)/.env sc_project/sc_project/
ln -sf $(pwd)/.env postgresql/

echo '.env generated (symbolic links sc_project/sc_project/.env , postgresql/.env)'
