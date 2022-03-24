from senpy.out.parser import parse_file, write_file

out_lines = parse_file("..\\sample_files\\sample.out")
write_file(out_lines, "..\\tmp\\sample.out")
