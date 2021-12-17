from senpy.sqt.parser import read_file, write_file


h_lines, s_lines = read_file("C:\\Users\\diash\\PycharmProjects\\ip2_file_package\\sample_files\\190806_200ng_180m_01_Slot2-3_1_632_nopd.sqt")

write_file(h_lines, s_lines, "C:\\Users\\diash\\PycharmProjects\\ip2_file_package\\tmp\\190806_200ng_180m_01_Slot2-3_1_632_nopd.sqt")