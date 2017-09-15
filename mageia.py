# vi: ts=4 expandtab
#
#    Copyright (C) 2012 Canonical Ltd.
#    Copyright (C) 2012 Hewlett-Packard Development Company, L.P.
#    Copyright (C) 2012 Yahoo! Inc.
#
#    Author: Scott Moser <scott.moser@canonical.com>
#    Author: Juerg Haefliger <juerg.haefliger@hp.com>
#    Author: Joshua Harlow <harlowja@yahoo-inc.com>
#    Author: Joseph C Wang <joequant@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 3, as
#    published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from cloudinit.distros import rhel

from cloudinit import log as logging

LOG = logging.getLogger(__name__)


class Distro(rhel.Distro):
    def _dist_uses_systemd(self):
        return True
    def package_command(self, command, args=None, pkgs=None):
        if pkgs is None:
            pkgs = []
        if command == "install": 
            cmd = ['urpmi', "--allow-force", "--force"]
        elif command == "update-sources":
            cmd = ["urpmi.update", "-a"]

        if args and isinstance(args, str):
            cmd.append(args)
        elif args and isinstance(args, list):
            cmd.extend(args)

        pkglist = util.expand_package_list('%s-%s', pkgs)
        cmd.extend(pkglist)

        # Allow the output of this to flow outwards (ie not be captured)
        util.subp(cmd, capture=False)

    def update_package_sources(self):
        self._runner.run("update-sources", self.package_command,
                         [], freq=PER_INSTANCE)
