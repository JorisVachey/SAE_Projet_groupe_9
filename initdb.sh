#!/bin/bash

if flask exist-db; then
    echo "DB déjà initialisée"
else
    flask drop-db
    flask init-db
    flask loaddb
    echo "DB initialisée"
fi

flask run --host=0.0.0.0
