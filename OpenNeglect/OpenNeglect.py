# -*- coding: utf-8 -*-

"""OpenNeglect.OpenNeglect: provides entry point main()."""

__version__ = "0.3"

import argparse
import re
import sys
from ipaddress import ip_address
from os import environ
from pathlib import Path
from shutil import which
from subprocess import CompletedProcess, run
from typing import Tuple
from json import dumps

from markdown_table import Table
from tabulate import tabulate


def msg(message: str) -> str:
    return "[+] {0}".format(message)


def err_msg(message: str) -> str:
    return "[!] {0}".format(message)


def validate_input(args) -> ip_address:
    # determine if the input IP address is inface an IP
    ip = None

    try:
        # if no target host given
        if not args.target:
            # look for RHOST environ var
            if "RHOST" in environ.keys():
                print(msg("Using Environment variable for IP address"))
                ip = ip_address(environ["RHOST"])
        else:
            ip = ip_address(args.target)

    except ValueError:
        print(err_msg("Argument or environment variable was not a valid IP address"))
        sys.exit()

    # Input check file
    if args.markdown:
        if Path(args.markdown).is_dir():
            print(err_msg("Given argument is a path and not a file"))
            sys.exit()

    return ip


def enumdomusers(rpcclient_bin: str, target_ip: str) -> CompletedProcess:
    cmd = list()
    cmd.extend([rpcclient_bin])
    cmd.extend(["-U", ""])
    cmd.extend([target_ip])
    cmd.extend(["-c", "enumdomusers"])
    cmd.extend(["-N"])

    output = run(cmd, capture_output=True)

    return output


def parse(cmd_output: str) -> list:
    regex = r"user:\[(\w+)]\srid:\[(\w+)\]"
    matches = re.findall(regex, cmd_output)
    ret_list = [{"user": m[0], "rid": m[1]} for m in matches if m]
    return ret_list


def userinfo_to_table(users: list) -> Tuple[list, list]:

    columns = ["Username", "rid", "hex_rid"]
    full_table = []

    for user in users:
        # create table
        full_table.append([user["user"], str(int(user["rid"], 16)), user["rid"]])

    return columns, full_table


def render_md_table(columns: list, full_table: list) -> str:
    return Table(columns, full_table).render()


def render_tab_table(columns: list, full_table: list) -> str:
    return tabulate(full_table, headers=columns, tablefmt="fancy_grid")


def main():
    print("Executing OpenNeglect version %s." % __version__)
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", help="IP address for target.")
    parser.add_argument("--markdown", help="Markdown File to append data.")
    parser.add_argument("--json", help="JSON file to write data.")
    args = parser.parse_args()

    ip = validate_input(args)

    if not ip:
        print(err_msg("Check IP argument"))
        sys.exit(-1)

    rpcclient_bin = which("rpcclient")
    if not rpcclient_bin:
        print(err_msg("Unable to locate rpcclient binary"))
        sys.exit(1)

    print(msg("rpcclient binary : {0}".format(rpcclient_bin)))

    cmd_output = enumdomusers(rpcclient_bin, str(ip))
    if cmd_output.returncode:
        print(err_msg("Rpcclient returned with an error code"))
        print("Error : {0}\nOutput : {1}".format(cmd_output.stderr, cmd_output.stdout))
        sys.exit(1)

    print(msg("Parsing Output returned from enumdomusers"))
    output = parse(str(cmd_output.stdout))

    if not output:
        print(err_msg("Was unable to parse information from rpcclient output"))
        sys.exit(1)

    print(msg("Located {0} users".format(len(output))))

    # create column and output data
    columns, table = userinfo_to_table(output)

    # if json argument given then write to file
    if args.json:
        print(msg("Writing json to file"))
        with open(args.json, "w") as json_file:
            json_file.write(dumps(output, indent=4))

    # if Output file given then write output to it
    if args.markdown:
        print(msg("Writing markdown to file"))
        md_table = render_md_table(columns, table)

        with open(args.markdown, "a+") as markdown_file:
            markdown_file.write("\n")
            markdown_file.write(md_table)

    print(msg("User Enumeration"))
    tabulate_table = render_tab_table(columns, table)

    print(tabulate_table)
