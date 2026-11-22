#!/usr/bin/env bash
# Cambia los colores verdes de GitHub del Pac-Man por la paleta del perfil.
set -euo pipefail
dark=dist/pacman-contribution-graph-dark.svg
light=dist/pacman-contribution-graph.svg

sed -i -E \
  -e 's/#0d1117/#1A0B2E/gI' \
  -e 's/#161b22/#2D1648/gI' \
  -e 's/#0e4429/#7B2CBF/gI' \
  -e 's/#006d32/#FF2E97/gI' \
  -e 's/#26a641/#FF8C42/gI' \
  -e 's/#39d353/#FFC857/gI' \
  -e 's/#ffffff/#C4B5FD/gI' \
  -e 's/#8b949e/#C4B5FD/gI' \
  "$dark"

sed -i -E \
  -e 's/#ebedf0/#F3E8FF/gI' \
  -e 's/#9be9a8/#C084FC/gI' \
  -e 's/#40c463/#FF2E97/gI' \
  -e 's/#30a14e/#FF8C42/gI' \
  -e 's/#216e39/#7B2CBF/gI' \
  -e 's/#000000/#7B2CBF/gI' \
  -e 's/#57606a/#6B21A8/gI' \
  "$light"
