from src.senpy.dtaSelectFilter.parser import read_file, write_file


_1, fpr, _2 = read_file("..\sample_files\DTASelect-filter.txt")

write_file(_1, fpr, _2, "..\\tmp\\DTASelect-filter.txt")

