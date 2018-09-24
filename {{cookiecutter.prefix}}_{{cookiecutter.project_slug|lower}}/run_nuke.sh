here="$(dirname `realpath $0`)"
out_path="$HOME/.nuke/tools/{{cookiecutter.prefix}}_{{cookiecutter.project_slug|lower}}"
cp -r $here $out_path
nukex
rm -rf $out_path;

