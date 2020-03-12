# OpenNeglect

Simple wrapper script to help standardize rpcclient output.

# Usage

Perform rpcclient -U "" 1.1.1.1 -N  and pipe output to json file and stdout

    OpenNeglect --target 1.1.1.1 --json scans/enumusers.json

Perform same scan accept write markdown table to text file as well as 
takes target from environment variable RHOST if set.

    OpenNeglect --markdown notes.txt --json scans/enumusers.json

# Future todos

* Pull in username and password
* Replace tag with output data in file

