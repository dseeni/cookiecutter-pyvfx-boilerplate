INFO = """
{{cookiecutter.prefix}}_{{cookiecutter.project_slug|lower}} successfully created.

FOR MAYA:

add this to you shell:
import {{cookiecutter.project_slug|lower}}.main as {{cookiecutter.project_slug|lower}}
{{cookiecutter.project_slug|lower}}.run_maya()

FOR NUKE:
simply move the {{cookiecutter.prefix}}_{{cookiecutter.project_slug|lower}} folder to $NUKEPATH

STANDALONE:
import {{cookiecutter.project_slug|lower}}.main as {{cookiecutter.project_slug|lower}}
{{cookiecutter.project_slug|lower}}.run_standalone()

"""


print(INFO)