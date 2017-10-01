# munin-node

## Introduction

This software is an alternative implementation of [https://github.com/munin-monitoring/munin-node-win32](https://github.com/munin-monitoring/munin-node-win32). Mostly because the old one was last updated 2015.

## Deployment

Install Python3 (not 2!), run `py munin-node.py`. Thats all. The program will listen on the default port 4949.

## Kown issues & limitations

- The command `list $nodename` and `list` are identical.
- Putty and the Windows `telnet` command do not work properly when connnecting to the listened port

## Contributing

Every plugin is located on `/plugins`. The program will register new Python based extensions on runtime.

The filename should be equals the class name. Also, each class should offer the non-static methods `config` and `fetch`. Both of these functions should return strings.

## License 

This program is licensed under the terms and conditions of the GNU General Public License.

