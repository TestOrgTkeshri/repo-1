import fnmatch

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as build_py_orig

excluded = ["django_models/tests/test_*.py"]


class BuildPy(build_py_orig):
    def find_package_modules(self, package, package_dir):
        """
        Overriding find_package_modules method to exclude test modules and settings from packaging
        """
        modules = super().find_package_modules(package, package_dir)
        return [
            (pkg, mod, file)
            for (pkg, mod, file) in modules
            if not any(fnmatch.fnmatchcase(file, pat=pattern) for pattern in excluded)
        ]


with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="django_models",
    include_package_data=True,
    packages=find_packages(),
    install_requires=required,
    cmdclass={"build_py": BuildPy}
)
