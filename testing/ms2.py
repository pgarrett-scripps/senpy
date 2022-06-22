from src.senpy.ms2.parser import read_file, write_file


h_lines, ms2_spectras = read_file("C:\\Users\\Ty\\Downloads\\prolucid_crash_gadi_2\\GB21_0099_deconv_dataAnalysis_Top150mix_glycoModified_noTrunk.ms2")

for ms2_spectra in ms2_spectras:
    if len(ms2_spectra.peak_lines) <= 10:
        print(ms2_spectra)
    if len(ms2_spectra.i_lines) == 0:
        print(ms2_spectra)
    if ms2_spectra.s_line == None:
        print(ms2_spectra)
    if ms2_spectra.z_line == None:
        print(ms2_spectra)
    rt = ms2_spectra.get_retention_time()
    ook0 = ms2_spectra.get_ook0()
    #print(rt, ook0)
#write_file(h_lines, s_lines, "C:\\Users\\Ty\\Downloads\\prolucid_crash_gadi_2\\GB21_0099_deconv_dataAnalysis_Top150mix_glycoModified_noTrunk_out.ms2")
