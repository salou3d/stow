#!/bin/sh
[ "${TERM:-none}" = "linux" ] && \
    printf '%b' '\e]P0{base00}}
                 \e]P1{base01}}
                 \e]P2{base02}}
                 \e]P3{base03}}
                 \e]P4{base04}}
                 \e]P5{base05}}
                 \e]P6{base05}}
                 \e]P7{base07}}
                 \e]P8{base08}}
                 \e]P9{base09}}
                 \e]PA{base0A}}
                 \e]PB{base0B}}
                 \e]PC{base0B}}
                 \e]PD{base0D}}
                 \e]PE{base0E}}
                 \e]PF{base0F}}
                 \ec'
