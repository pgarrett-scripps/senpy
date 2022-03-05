from sqt import read_file, write_file


h_lines, s_lines = read_file("C:\\Users\\diash\\PycharmProjects\\ip2_file_package\\sample_files\\sample_timscore.sqt")

write_file(h_lines, s_lines, "C:\\Users\\diash\\PycharmProjects\\ip2_file_package\\tmp\\sample_timscore.sqt")