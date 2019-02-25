import sys


def print_hex_string(str):
    result = ""
    for i in str:
        result += hex(ord(i))
    return result


def convert_mem_to_16(string):
    cur = 0
    target = list(string)
    for i in target[::-1]:
        cur = cur << 8 | i
    return cur


def get_byte_from_file(fp, size):
    result = fp.read(size)
    result = convert_mem_to_16(result)

    return result


def print_hex_dump(buffer, start_offset=0):
    print('-' * 79)

    offset = 0
    while offset < len(buffer):
        # Offset
        print(' %08X : ' % (offset + start_offset), end='')

        if ((len(buffer) - offset) < 0x10) is True:
            data = buffer[offset:]
        else:
            data = buffer[offset:offset + 0x10]

        # Hex Dump
        for hex_dump in data:
            print("%02X" % hex_dump, end=' ')

        if ((len(buffer) - offset) < 0x10) is True:
            print(' ' * (3 * (0x10 - len(data))), end='')

        print('  ', end='')

        # Ascii
        for ascii_dump in data:
            if ((ascii_dump >= 0x20) is True) and ((ascii_dump <= 0x7E) is True):
                print(chr(ascii_dump), end='')
            else:
                print('.', end='')

        offset = offset + len(data)
        print('')

    print('-' * 79)


class property:
    def __init__(self, block):
        assert len(block) == 0x80
        self.name_size = convert_mem_to_16(block[0x40: 0x42])
        self.name = block[:self.name_size]
        self.name = self.name.decode('UTF-8')
        self.type = block[0x42]

        if self.type == 0x1:
            self.type = [0x1, "storage"]
        elif self.type == 0x2:
            self.type = [0x2, "stream"]
        else:
            self.type = [0x5, "root"]
        self.prev_prop = convert_mem_to_16(block[0x44: 0x48])
        self.next_prop = convert_mem_to_16(block[0x48: 0x4C])
        self.dirc_prop = convert_mem_to_16(block[0x4C: 0x50])

        self.starting_block_of_prop = convert_mem_to_16(block[0x74: 0x78])
        self.size_of_property = convert_mem_to_16(block[0x78: 0x7C])

    def info(self):
        print("name : " + self.name)
        print("type = " + str(self.type[0]) + " " + self.type[1])
        print("starting block of property : " + hex(self.starting_block_of_prop))
        print("size of property : " + hex(self.size_of_property) + "\n")


class OLE:
    BBAT = b""
    storages = {}
    stream = []
    propertys = []
    ROOT = None
    def __init__(self, file_name):
        self.fp = open(file_name, 'rb')
        self.com_header_signature = self.fp.read(8)
        if self.com_header_signature != b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1':
            print("WRONMG")
            print(self.com_header_signature)
            return

        self.com_header_CLSID = get_byte_from_file(self.fp, 16)
        self.minor_version = get_byte_from_file(self.fp, 2)
        self.major_version = get_byte_from_file(self.fp, 2)
        self.byte_order = get_byte_from_file(self.fp, 2)
        self.sector_shift = get_byte_from_file(self.fp, 2)
        self.mini_sector_shift = get_byte_from_file(self.fp, 2)
        self.reserved = get_byte_from_file(self.fp, 6)
        self.number_of_directory_sector = get_byte_from_file(self.fp, 4)
        self.number_of_fat_sector = get_byte_from_file(self.fp, 4)
        self.first_directory_sector_location = get_byte_from_file(self.fp, 4)
        self.transaction_signature_number = get_byte_from_file(self.fp, 4)
        self.mini_stream_cutoff_size = get_byte_from_file(self.fp, 4)
        self.first_mini_fat_sector_location = get_byte_from_file(self.fp, 4)
        self.number_of_mini_fat_sector = get_byte_from_file(self.fp, 4)
        self.first_DIFAT_sector_location = get_byte_from_file(self.fp, 4)
        self.number_of_DIFAT_sector = get_byte_from_file(self.fp, 4)
        self.DIFAT = []
        for i in range(109):
            cur = get_byte_from_file(self.fp, 4)
            self.DIFAT.append(cur)

    def info(self):
        print("===Header Information===")
        print("CLSID = " + hex(self.com_header_CLSID))
        print("Minor Version = " + hex(self.minor_version))
        print("Majolr Version = " + hex(self.major_version))
        print("Byte Orfer = " + hex(self.byte_order))
        print("Reserved = " + hex(self.reserved))
        print("Sector Shift = " + hex(self.sector_shift))
        print("Mini Sector Shift = " + hex(self.mini_sector_shift))

        print("Number of Directory Sectors = " + hex(self.number_of_directory_sector))
        print("Number 0f FAT sector number = " + hex(self.number_of_fat_sector))
        print("First directyory sector Location = " + hex(self.first_directory_sector_location))
        print("Transaction Signature Number = " + hex(self.transaction_signature_number))
        print("Mini Stream Cutoff Size = " + hex(self.mini_stream_cutoff_size))
        print("First mini Fat Sector Location = " + hex(self.first_mini_fat_sector_location))
        print("Number of Mini FAT Sector = " + hex(self.number_of_mini_fat_sector))
        print("First DIFAT Sector Location = " + hex(self.first_DIFAT_sector_location))
        print("Number 0f DIFAT sector number = " + hex(self.number_of_DIFAT_sector))
        print("DIFAT :")
        for i, di in enumerate(self.DIFAT):
            print("DIFAT[" + str(i) + "] = 0x{:08x}".format(di))

    def read_block(self, block_idx):
        self.fp.seek(0x200 * (block_idx + 1))
        block_content = self.fp.read(0x200)
        return block_content

    def get_BBAT(self):
        #One block size = 0x200
        for i in range(self.number_of_fat_sector):
            cur_block_idx = hwp_ole.DIFAT[i]
            self.BBAT += self.read_block(cur_block_idx)
    def get_SBAT(self):
        #One block size = 0x40
        #fitst mini fat secgtor location
        #number of mini fat sector
        cur_len = len(self.stream)
        self.get_stream(self.first_mini_fat_sector_location, self.BBAT)
        print(self.stream[cur_len])
        self.build_storage('SBAT', self.stream[cur_len])

    def get_root_data(self):
        return

    def get_stream(self, start_index, table):
        cur_chain = []
        entry = start_index
        cur_chain.append(entry)

        while 1:
            entry = table[4 * entry: 4 * (entry + 1)]
            entry = convert_mem_to_16(entry)
            if entry == 0xfffffffe:
                break
            cur_chain.append(entry)
        self.stream.append(cur_chain)

    def build_storage(self, storage_name, chain, root = None):
        cur_content = b""
        if root == None:
            for i in chain:
                cur_content += self.read_block(i)
            self.storages[storage_name] = cur_content
        else:
            for i in chain:
                cur_content += root[i * 0x40 : (i + 1) * 0x40]
            self.storages[storage_name] = cur_content

    def read_from_root(self, i):
        cur_content = b""


hwp_ole = OLE("h.hwp")

hwp_ole.info()

hwp_ole.get_BBAT()
hwp_ole.get_SBAT()



hwp_ole.get_stream(hwp_ole.first_directory_sector_location, hwp_ole.BBAT)
hwp_ole.build_storage("Property_Storage", hwp_ole.stream[1])


for i in range(len(hwp_ole.stream[0] * 4)):
    cur_data = hwp_ole.storages['Property_Storage']
    pr = property(cur_data[i * 0x80: (i + 1) * 0x80])
    if pr.name_size == 0x0:
        continue
    hwp_ole.propertys.append(pr)

def get_pr_data(pr):
    if pr.type[0] == 0x1:
        print(pr.name + "is storage")

    if pr.size_of_property < 0x1000:
        cur_len = len(hwp_ole.stream)
        hwp_ole.get_stream(pr.starting_block_of_prop, hwp_ole.storages['SBAT'])
        hwp_ole.build_storage(pr.name, hwp_ole.stream[cur_len], root=hwp_ole.ROOT)

    else:
        cur_len = len(hwp_ole.stream)
        hwp_ole.get_stream(pr.starting_block_of_prop, hwp_ole.BBAT)
        hwp_ole.build_storage(pr.name, hwp_ole.stream[cur_len])


for i, pr in enumerate(hwp_ole.propertys):
    if i == 0:
        #root directory data
        get_pr_data(pr)
        hwp_ole.ROOT = hwp_ole.storages[pr.name]

    get_pr_data(pr)

for i in hwp_ole.storages:
    print(i)

for i in hwp_ole.propertys:
    print("\n=========" + i.name + "===========\n")
    print_hex_dump(hwp_ole.storages[i.name])
    input(">>>")
