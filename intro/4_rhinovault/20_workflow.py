import pathlib

from compas_session.lazyload import LazyLoadSession

HERE = pathlib.Path(__file__).parent

session = LazyLoadSession(name="RV", basedir=HERE, delete_existing=True)
