"""
This file is part of dbdump.

Copyright 2009, 2010 Mathias Ertl

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from libdump import backend
from subprocess import *

class postgresql(backend.backend):
    def get_db_list(self):
        cmd = [ 'psql', '-Aqt', '-c', '"select datname from pg_database"' ]

        if 'psql_opts' in self.section:
            cmd += self.section['psql_opts'].split(' ')

        if 'su' in self.section:
            cmd = [ 'su', 'postgres', '-s', '/bin/bash', '-c', ' '.join(cmd) ]

        p_list = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p_list.communicate()
        databases = [ line for line in stdout.decode().strip().split("\n") if line != 'template0' ]

        p_list.wait()
        if p_list.returncode != 0:
            raise Exception("Unable to get list of databases: %s "
                % (stderr.decode().strip("\n")))

        return databases

    def get_command(self, database):
        cmd = [ 'pg_dump', '-c' ]
        if 'pgdump_opts' in self.section:
            cmd += self.section['pgdump_opts'].split(' ')
        cmd.append(database)
        return cmd

