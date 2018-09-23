here="$(dirname `realpath $0`)"
out_path="$HOME/.nuke/plugins/NUKE_PANEL_{{cookiecutter.project_slug|lower}}_NUKE112"
rm -rf $out_path;
cp -r $here $out_path
nukex

