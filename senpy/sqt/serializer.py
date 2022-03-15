from senpy.util import LineSerializer
from senpy.sqt.exceptions import SqtFileDeserializationLLineException, SqtFileDeserializationMLineException, \
    SqtFileDeserializationSLineException
from senpy.sqt.lines import SLine, MLine, LLine


class LLineSerializer(LineSerializer):
    @staticmethod
    def deserialize(line: str) -> LLine:
        line_elements = line.rstrip().split("\t")
        if len(line_elements) < 4:
            raise SqtFileDeserializationLLineException(_line=line)
        locus_name = None if line_elements[1] == 'NA' else line_elements[1]
        peptide_index_in_protein_sequence = None if line_elements[2] == 'NA' else int(line_elements[2])
        peptide_sequence = None if line_elements[3] == 'NA' else line_elements[3]

        l_line = LLine(locus_name, peptide_index_in_protein_sequence, peptide_sequence)
        return l_line

    @staticmethod
    def serialize(l_line: LLine) -> str:
        line_elements = ["L",
                         "NA" if l_line.locus_name is None else l_line.locus_name,
                         "NA" if l_line.peptide_index_in_protein_sequence is None
                         else l_line.peptide_index_in_protein_sequence,
                         "NA" if l_line.peptide_sequence is None else l_line.peptide_sequence
                         ]

        line_elements = [str(elem) for elem in line_elements]

        return '\t'.join(line_elements) + '\n'


class MLineSerializer(LineSerializer):
    @staticmethod
    def deserialize(line: str) -> MLine:
        line_elements = line.rstrip().split("\t")
        if len(line_elements) < 11:
            raise SqtFileDeserializationMLineException(_line=line)
        xcorr_rank = None if line_elements[1] == 'NA' else int(line_elements[1])
        sp_rank = None if line_elements[2] == 'NA' else int(line_elements[2])
        calculated_mass = None if line_elements[3] == 'NA' else float(line_elements[3])
        DeltaCN = None if line_elements[4] == 'NA' else float(line_elements[4])
        xcorr = None if line_elements[5] == 'NA' else float(line_elements[5])
        sp = None if line_elements[6] == 'NA' else float(line_elements[6])
        matched_ions = None if line_elements[7] == 'NA' else int(line_elements[7])
        expected_ions = None if line_elements[8] == 'NA' else int(line_elements[8])
        sequence = None if line_elements[9] == 'NA' else line_elements[9]
        validation_status = None if line_elements[10] == 'NA' else line_elements[10]

        # Handle SQT and/or Timsscore SQT
        predicted_ook0 = None
        tims_score = None
        tims_b_score_m2 = None
        tims_b_score_best_m = None
        if len(line_elements) >= 13:  # Timsscore
            predicted_ook0 = None if line_elements[11] == 'NA' else float(line_elements[11])
            tims_score = None if line_elements[12] == 'NA' else float(line_elements[12])
        if len(line_elements) >= 15:  # additional TimsScores
            tims_b_score_m2 = None if line_elements[13] == 'NA' else float(line_elements[13])
            tims_b_score_best_m = None if line_elements[14] == 'NA' else float(line_elements[14])

        m_line = MLine(xcorr_rank, sp_rank, calculated_mass, DeltaCN, xcorr, sp, matched_ions, expected_ions,
                       sequence, validation_status, predicted_ook0, tims_score,
                       tims_b_score_m2, tims_b_score_best_m)
        return m_line

    @staticmethod
    def serialize(m_line: MLine) -> str:
        line_elements = ["M",
                         "NA" if m_line.xcorr_rank is None else m_line.xcorr_rank,
                         "NA" if m_line.sp_rank is None else m_line.sp_rank,
                         "NA" if m_line.calculated_mass is None else round(float(m_line.calculated_mass), 5),
                         "NA" if m_line.DeltaCN is None else round(float(m_line.DeltaCN), 4),
                         "NA" if m_line.xcorr is None else round(float(m_line.xcorr), 4),
                         "NA" if m_line.sp is None else round(float(m_line.sp), 3),
                         "NA" if m_line.matched_ions is None else m_line.matched_ions,
                         "NA" if m_line.expected_ions is None else m_line.expected_ions,
                         "NA" if m_line.sequence is None else m_line.sequence,
                         "NA" if m_line.validation_status is None else m_line.validation_status,
                         "NA" if m_line.predicted_ook0 is None else round(float(m_line.predicted_ook0), 4),
                         "NA" if m_line.tims_score is None else round(float(m_line.tims_score), 4),
                         "NA" if m_line.tims_b_score_m2 is None else round(float(m_line.tims_b_score_m2), 4),
                         "NA" if m_line.tims_b_score_best_m is None else round(float(m_line.tims_b_score_best_m), 4)
                         ]

        line_elements = [str(elem) for elem in line_elements]

        return '\t'.join(line_elements) + '\n'


class SLineSerializer(LineSerializer):
    @staticmethod
    def deserialize(line: str) -> SLine:
        line_elements = line.rstrip().split("\t")
        if len(line_elements) < 10:
            raise SqtFileDeserializationSLineException(_line=line)
        low_scan = None if line_elements[1] == 'NA' else int(line_elements[1].rstrip())
        high_scan = None if line_elements[2] == 'NA' else int(line_elements[2].rstrip())
        charge = None if line_elements[3] == 'NA' else int(line_elements[3].rstrip())
        process_time = None if line_elements[4] == 'NA' else int(line_elements[4].rstrip())
        server = None if line_elements[5] == 'NA' else line_elements[5].rstrip()
        experimental_mass = None if line_elements[6] == 'NA' else float(line_elements[6].rstrip())
        total_ion_intensity = None if line_elements[7] == 'NA' else float(line_elements[7].rstrip())
        lowest_sp = None if line_elements[8] == 'NA' else float(line_elements[8].rstrip())
        number_matches = None if line_elements[9] == 'NA' else int(line_elements[9].rstrip())

        experimental_ook0 = None
        experimental_mz = None
        corrected_ook0 = None
        if len(line_elements) >= 11:
            experimental_ook0 = None if line_elements[10] == 'NA' else float(line_elements[10].rstrip())

        if len(line_elements) >= 12:
            experimental_mz = None if line_elements[11] == 'NA' else float(line_elements[11].rstrip())

        if len(line_elements) >= 13:
            corrected_ook0 = None if line_elements[12] == 'NA' else float(line_elements[12].rstrip())

        s_line = SLine(low_scan, high_scan, charge, process_time, server, experimental_mass, total_ion_intensity,
                       lowest_sp, number_matches, experimental_ook0, experimental_mz, corrected_ook0)
        return s_line

    @staticmethod
    def serialize(s_line: SLine) -> str:
        line_elements = ["S",
                         "NA" if s_line.low_scan is None else s_line.low_scan,
                         "NA" if s_line.high_scan is None else s_line.high_scan,
                         "NA" if s_line.charge is None else s_line.charge,
                         "NA" if s_line.process_time is None else s_line.process_time,
                         "NA" if s_line.server is None else s_line.server,
                         "NA" if s_line.experimental_mass is None else round(float(s_line.experimental_mass), 5),
                         "NA" if s_line.total_ion_intensity is None else round(float(s_line.total_ion_intensity), 2),
                         "NA" if s_line.lowest_Sp is None else round(float(s_line.lowest_Sp), 4),
                         "NA" if s_line.number_matches is None else s_line.number_matches,
                         "NA" if s_line.experimental_ook0 is None else round(float(s_line.experimental_ook0), 5),
                         "NA" if s_line.experimental_mz is None else round(float(s_line.experimental_mz), 5),
                         "NA" if s_line.corrected_ook0 is None else round(float(s_line.corrected_ook0), 5)]

        line_elements = [str(elem) for elem in line_elements]

        return '\t'.join(line_elements) + '\n'
