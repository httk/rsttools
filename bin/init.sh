################################################################################
#
# This script is part of rstslide. Its purpose is to set up the
# environment for bash.
#
# Just run (or add to your init files)
#   source /path/to/rstslide/bin/init.sh
#
################################################################################

HERE="${BASH_SOURCE[0]}"
eval HEREDIR="$(dirname "$HERE")"
DIR="$(cd "$HEREDIR/.."; pwd -P)"
export PATH="$DIR/bin:$PATH"
export PYTHONPATH="$DIR/rstslide/src:$PYTHONPATH"
