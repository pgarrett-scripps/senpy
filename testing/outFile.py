from senpy.out.parser import read_file, write_file

out_lines = read_file("..\\sample_files\\sample.out")
write_file(out_lines, "..\\tmp\\sample.out")
