#!/usr/bin/env bash

overlay_create()
{
    #free=$((`stat -c '%a*%S/1024/1024' -f .`))
    #echo free ${free}M
    overlay_remove "$@"
    for d in "$@"; do
        b="$(basename $d)"
        size_bkl=$(blockdev --getsz "$d") # in 512 blocks/sectors
        # reserve 1M space for snapshot header.  note: ext3 max file length is 2TB
        truncate -s$((((size_bkl+1)/2)+1024))K "$b".ovr || (echo "Do you use ext4?"; return 1)
        loop=$(losetup -f --show -- "$b".ovr)
        # https://www.kernel.org/doc/Documentation/device-mapper/snapshot.txt
        dmsetup create "$b" --table "0 $size_bkl snapshot $d $loop P 8"
        echo "$d" $((size_bkl/2048))M "$loop" /dev/mapper/"$b"
    done
}

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

overlay_create "$@"
