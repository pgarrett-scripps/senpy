from senpy.sqt.parser import read_file, write_file


h_lines, s_lines = read_file("C:\\Users\\ty\\repos\\senpy_package\\sample_files\\sample_timscore.sqt", version="v2.1.0")
write_file(h_lines, s_lines, "C:\\Users\\ty\\repos\\senpy_package\\tmp\\sample_timscore.sqt", version="v2.1.0")

h_lines, s_lines = read_file("C:\\Users\\ty\\repos\\senpy_package\\sample_files\\sample.sqt", version="v1.4")
write_file(h_lines, s_lines, "C:\\Users\\ty\\repos\\senpy_package\\tmp\\sample.sqt", version="v1.4")