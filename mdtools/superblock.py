from . import namedfilestruct
import struct

class Superblock(namedfilestruct.NamedFileStruct):
    offset = 4096
    endian = '='
    fields = dict(
        # superblock identification area
        magic = 'I',
        major_version = 'I',
        feature_map = 'I',
            # features
            # 1 RAID bitmap is used
            # 2 RAID recovery is in progress (recovery_offset)
            # 4 RAID reshape is in progress
            # 8,16 -> undefined/reserved
        pad0 = 'I', # always written zero

        # per-array identification and configuration area
        set_uuid = '16s',
        set_name = '32s',
        ctime = 'Q', # low 40 bits are seconds; high 24 bits are microseconds
        level = 'I', 
            # levels:
            # -4: multi-path
            # -1: linear
            # 0, 1, 4, 5, 6, 0xA: raid level
        layout = 'I',
            # layouts: (relative arrangement of data and parity blocks on the disks)
            # 0: left asymmetric
            # 1: right asymmetric
            # 2: left symmetric (default)
            # 3: right symmetric
            # 0x0102: raid-10
            # 0x0100: offset2
        size = 'Q', # component size in 512-byte sectors
        chunksize = 'I', # in 512-byte sectors, usually 64k by default [seems to be made as 1k rather than 512?]
        raid_disks = 'I', # number of disks in array
        bitmap_offset = 'i', # position of bitmap relative to superblock, in sectors

        # reshape in-process metadata storage/recovery area
        # only used if feature_map bit 4 is set
        new_level = 'I',
        reshape_position = 'Q',
        delta_disks = 'I',
        new_layout = 'I',
        new_chunk = 'I',
        pad1 = 'I', # written zero

        # this component device information area
        data_offset = 'Q', # sector # where data begins
        data_size = 'Q', # no. of sectors that can be/are used for data
        super_offset = 'Q', # sector where this superblock starts
        recovery_offset = 'Q', # sectors after data_offset where recovery is at?
        dev_number = 'I', # device identifier number
        cnt_corrected_read = 'I', # number of read-errors corrected by rewriting
        device_uuid = '16s', # uuid of the component device
        devflags = 'B', 
            # flags
            # 1 WriteMostly1
            # ... ?
            # text on this section was cut off on right
        pad2 = '7s', # written as zeros

        # array-state information area
        # offsert=0xc0, 64 bytes
        utime = 'Q', # time of last superblock update.  high 24-bits are microseconds
        events = 'Q', # event count, incremented whenever superblock updated, to detect sync'd disks
        resync_offset = 'Q', # sync position after data_offset
        sb_csum = 'I', # up to devs[max_dev]
        max_dev = 'I', # number of devices in the array
        pad3 = '32s', # always written zero

        # device roles (positions in array) area follows, 1 per device
    )
    dev_role_field = 'H' # 0xfffe means spare; 0xffff means faulty; others are position/role
    def read(self, *params, **kwparams):
        super().read(*params, **kwparams)
        self.values['dev_roles'] = list(struct.iter_unpack('H', self.fileobj.read(2 * self.max_dev)))


if __name__ == '__main__':
    import sys
    with open(sys.argv[-1], 'rb') as fileobj:
        superblock = Superblock(fileobj)
        print(superblock.values)
