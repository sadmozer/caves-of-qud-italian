#!/bin/bash
set -e

BAT="$(dirname "$0")/install_mod.bat"
BAT_WIN="$(wslpath -w "$(realpath "$BAT")")"

cmd.exe /c "$BAT_WIN"
