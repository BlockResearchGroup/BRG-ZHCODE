#! python3
# venv: zha-intro-rhino
# r: compas, compas_cgal, compas_libigl

import compas
import compas_cgal
import compas_libigl


def check_version(package, version):
    print(f"{version:<7} => {package.__version__:<7} {'OK' if package.__version__ == version else 'ERROR'}")


check_version(compas, "2.13.0")
check_version(compas_cgal, "0.9.0")
check_version(compas_libigl, "0.6.0")
