#!/bin/bash

rsync -avz {webapp.py,russian_syntags.mco,maltparser-1.9.1.jar,lib,template.html} \
    neurolab:webapp/
