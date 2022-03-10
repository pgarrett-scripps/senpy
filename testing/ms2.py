from senpy.ms2.parser import read_file, write_file


h_lines, s_lines = read_file("..\\sample_files\\sample.ms2")

write_file(h_lines, s_lines, "..\\sample_files\\sample_out.ms2")