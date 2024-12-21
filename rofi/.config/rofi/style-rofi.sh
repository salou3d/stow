#!/usr/bin/env bash

dir="$HOME/.config/rofi/launchers/"
previews="$HOME/Documents/rofi/previews/launchers"

styles=$(echo $previews/type-[1-7])
mystyles=""
for style in $styles; do
    types=$(ls $style)
    for type in $types; do
        mystyles="$style/$type\n$mystyles"
    done
done


mytype=$(printf $mystyles | fzf +m --sort --preview 'fzf-preview.sh {}')

if [ ! -z "$mytype" -a -f "$mytype" ]; then
    st=$(echo "$mytype" | awk -F '/' '{print $(NF-1)}')
    tp=$(echo "$mytype" | awk -F '/' '{split($NF, A, /\./); print A[1]}')
    echo "$st/type-$tp"
    rofi \
    -show drun \
    -theme ${dir}/"$st/style-$tp".rasi
fi
