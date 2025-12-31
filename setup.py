"""Custom setup to ensure binaries have executable permissions."""

import stat
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py


class BuildPyWithExecutables(build_py):
    """Custom build_py that sets executable permissions on binaries."""

    def run(self):
        super().run()
        # Make binaries executable in the build directory
        build_lib = Path(self.build_lib)
        for binary in build_lib.glob("clippit/bin/*/clippit-compare"):
            if binary.is_file():
                current_mode = binary.stat().st_mode
                binary.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


setup(cmdclass={"build_py": BuildPyWithExecutables})
