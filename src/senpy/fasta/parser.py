from Bio import SeqIO

def read_file(fasta_file_path):
    records = []
    for record in SeqIO.parse(fasta_file_path, "fasta"):
        # record options: 'annotations', 'dbxrefs', 'description', 'features', 'format', 'id', 'letter_annotations', 'lower', 'name', 'reverse_complement', 'seq', 'translate', 'upper']
        records.append(record)
    records_dict = {i: record for i, record in enumerate(records)}
    return records_dict


def write_file(fasta_file_path, records_dict, protein_sequence_line_length=60) -> None:
    with open(fasta_file_path, "w") as file:
        for record_itr in records_dict:
            record = records_dict[record_itr]
            file.write(str(record.description) + "\n")
            for i in range(0, len(str(record.seq)), protein_sequence_line_length):
                partial_sequence = str(record.seq)[i:i+protein_sequence_line_length]
                file.write(str(partial_sequence) + "\n")
