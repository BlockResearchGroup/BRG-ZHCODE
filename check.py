import compas
import compas_cgal
import compas_gmsh
import compas_libigl
import compas_model
import compas_occ
import compas_viewer


def check_version(package, version):
    print(f"{version:<7} => {package.__version__:<7} {'OK' if package.__version__ == version else 'ERROR'}")


check_version(compas, "2.13.0")
check_version(compas_cgal, "0.9.0")
check_version(compas_gmsh, "0.4.2")
check_version(compas_libigl, "0.6.0")
check_version(compas_model, "0.7.0")
check_version(compas_occ, "1.2.1")
check_version(compas_viewer, "1.5.0")
