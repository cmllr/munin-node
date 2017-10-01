# munin-node

## Introduction

This software is an alternative implementation of [https://github.com/munin-monitoring/munin-node-win32](https://github.com/munin-monitoring/munin-node-win32). Mostly because the old one was last updated 2015.

## Deployment

Install Python3 (not 2!), run `py munin-node.py`. Thats all. The program will listen on the default port 4949.

## Kown issues & limitations

- The command `list $nodename` and `list` are identical.
- Putty and the Windows `telnet` command do not work properly when connnecting to the listened port

## License 

This program is licensed under the terms and conditions of the GNU General Public License.

