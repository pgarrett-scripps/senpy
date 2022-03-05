from outFile.parser import parse_file, write_file

h_lines, out_lines = parse_file("C:\\Users\\diash\\PycharmProjects\\ip2_file_package\\sample_files\\sample.out")
write_file(h_lines, out_lines, "C:\\Users\\diash\\PycharmProjects\\ip2_file_package\\tmp\\sample.out")
