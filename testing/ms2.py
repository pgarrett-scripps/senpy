from senpy.ms2.parser import read_file, write_file


h_lines, s_lines = read_file("C:\\Users\\diash\\PycharmProjects\\ip2_file_package\\sample_files\\sample.ms2")

write_file(h_lines, s_lines, "C:\\Users\\diash\\PycharmProjects\\ip2_file_package\\tmp\\sample.ms2")