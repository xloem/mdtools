#!/usr/bin/env bash

overlay_remove()
{
    for d in "$@"; do
        b="$(basename "$d")"
        [ -e /dev/mapper/"$b" ] && dmsetup remove "$b" && echo /dev/mapper/"$b"
        if [ -e "$b".ovr ]; then
            echo "$b".ovr
            l="$(losetup -j "$b".ovr | cut -d : -f1)"
            echo "$l"
            [ -n "$l" ] && losetup -d "$l"
            rm -f "$b".ovr &> /dev/null
        fi
    done
}

overlay_remove "$@"
