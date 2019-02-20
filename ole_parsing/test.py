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

class COM:
    def __init__(self, fp):
        self.com_header_signature = fp.read(8)
        if self.com_header_signature != b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1':
            print("WRONMG")
            print(self.com_header_signature)
            return

        self.com_header_CLSID = get_byte_from_file(fp, 16)

        self.minor_version = get_byte_from_file(fp, 2)
        self.major_version = get_byte_from_file(fp, 2)

        self.byte_order = get_byte_from_file(fp, 2)
        self.sector_shift = get_byte_from_file(fp, 2)

        self.mini_sector_shift = get_byte_from_file(fp, 2)
        self.reserved = get_byte_from_file(fp, 6)
        self.number_of_directory_sector = get_byte_from_file(fp, 4)

        self.number_of_fat_sector = get_byte_from_file(fp, 4)
        self.first_directory_sector_location = get_byte_from_file(fp, 4)

        self.transaction_signature_number = get_byte_from_file(fp, 4)
        self.mini_stream_cutoff_size = get_byte_from_file(fp, 4)
        self.first_mini_fat_sector_location = get_byte_from_file(fp, 4)

        self.number_of_mini_fat_sector = get_byte_from_file(fp, 4)
        self.first_DIFAT_sector_location = get_byte_from_file(fp, 4)
        self.number_of_DIFAT_sector = get_byte_from_file(fp, 4)
        self.DIFAT =[]
        for i in range(109):
            cur = get_byte_from_file(fp, 4)
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



fp = open("hwp_test.hwp", 'rb')

hwp_com = COM(fp)
hwp_com.info()
