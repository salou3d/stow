#!/usr/bin/env bash

dir="$HOME/.config/rofi/applets/"
previews="$HOME/Documents/rofi/previews/applets"

styles=$(find "$previews" -type d | tail -n +2)

mystyles=""
for style in $styles; do
    types=$(ls $style)
    for type in $types; do
        mystyles="$style/$type\n$mystyles"
    done
done


mytype=$(printf $mystyles | fzf +m --sort --preview 'fzf-preview.sh {}')

echo $mytype

if [ ! -z "$mytype" -a -f "$mytype" ]; then
    st=$(echo "$mytype" | awk -F '/' '{print $(NF-1)}')
    tp=$(echo "$mytype" | awk -F '/' '{split($NF, A, /\./); print A[1]}')
    echo "$st/type-$tp"
    rofi \
    -show drun \
    -theme ${dir}/"$st/style-$tp".rasi
fi
