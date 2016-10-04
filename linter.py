# Written by Aparajita Fishman
# Contributors: Francis Gulotta, Josh Hagins, Mark Haylock
# Copyright (c) 2015-2016 The SublimeLinter Community
# Copyright (c) 2013-2014 Aparajita Fishman
# License: MIT
# Changed for CudaLint: Alexey T.

import os
from cuda_lint import Linter


class Rubocop(Linter):
    """Provides an interface to rubocop."""

    syntax = 'Ruby'
    cmd = None
    executable = 'ruby' 
    version_args = '-S rubocop --version'
    version_re = r'(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 0.34.0'
    regex = (
        r'^.+?:(?P<line>\d+):(?P<col>\d+): '
        r'(:?(?P<warning>[RCW])|(?P<error>[EF])): '
        r'(?P<message>.+)'
    )

    def cmd(self):
        """Build command, using STDIN if a file path can be determined."""
        command = ['ruby', '-S', 'rubocop', '--format', 'emacs']

        path = self.filename
        if not path:
            raise Exception('Cannot lint untitled tab: rubocop')
        
        if path:
            # With this path we can instead pass the file contents in via STDIN
            # and then tell rubocop to use this path (to search for config
            # files and to use for matching against configured paths - i.e. for
            # inheritance, inclusions and exclusions).
            #
            # The 'force-exclusion' overrides rubocop's behavior of ignoring
            # global excludes when the file path is explicitly provided:
            command += ['--force-exclusion', '--stdin', path]
            
        return command
