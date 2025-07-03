from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('sbe2.pygen', 'templates')
)

enum = env.get_template('enum.py.j2')
set_ = env.get_template('set.py.j2')
composite = env.get_template('composite.py.j2')