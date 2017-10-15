#!/bin/bash

rsync -vz {webapp.py,russian_syntags.mco,maltparser-1.9.1.jar,lib,template.html} \
    neurolab:webapp/
