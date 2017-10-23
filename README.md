# munin-node

## Introduction

This software is an alternative implementation of [https://github.com/munin-monitoring/munin-node-win32](https://github.com/munin-monitoring/munin-node-win32). Mostly because the old one was last updated 2015. Another things is that the old node needs VC++ 2008, which is painful to use.

## Installation

1. Install Python3 (not 2!)
2. Install the requirements listed in `requirements.txt`
3. Run `py munin-node.py`. 

### Why the **** did you use Python?

By using Python I could achieve the easiest solution for this task. Other languages also need a large toolchain to install, which is not needed when using Python. Also Python offers the advantage to develop it on Linux, too (even when the plugins won't work).

## Kown issues & limitations

- The command `list $nodename` and `list` are identical.
- Putty and the Windows `telnet` command do not work properly when connnecting to the listened port
- Not all configuration values are supported

## Configuration

In general, the plugin supports the settings listed on [http://guide.munin-monitoring.org/en/latest/reference/munin-node.conf.html](http://guide.munin-monitoring.org/en/latest/reference/munin-node.conf.html).

Yet there are some platform specific exceptions which are *not supported*:

- user
- group 
- ignore_file
- global_timeout
- background
- sid
- The Perl based Net::Server configurations
- pid_file

## Contributing

Every plugin is located in `/plugins`. The program will register new Python based extensions on runtime.

The filename should equal the class name. Also, each class should offer the non-static methods `config` and `fetch`. Both of these functions should return strings.

## License 

This program is licensed under the terms and conditions of the GNU General Public License v3.

