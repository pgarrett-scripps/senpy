from senpy.idx.utils import create_connection, convert_float, convert_int, BYTES_SIZE, END_INT_VALUE, \
    convert_int_to_bytes, convert_float_to_bytes
from senpy.idx.data import IdxInfo


class IdxSerializer:
    @staticmethod
    def deserialize(idx_db: str) -> [IdxInfo]:
        idx_info_list = []

        connection = create_connection(idx_db)
        c = connection.cursor()
        c.execute("SELECT * FROM blazmass_sequences")
        raw_data = c.fetchall()

        for ind in raw_data:
            data = ind[1]
            i = 0
            while i < (len(data)):
                precursorMass = convert_float(data[i:i + BYTES_SIZE])
                i += BYTES_SIZE
                seqOffset = convert_int(data[i:i + BYTES_SIZE])
                i += BYTES_SIZE
                seqLength = convert_int(data[i:i + BYTES_SIZE])
                i += BYTES_SIZE

                protein_ids = []
                converted_int = convert_int(data[i:i + BYTES_SIZE])
                while converted_int != END_INT_VALUE:
                    protein_ids.append(converted_int)
                    i += BYTES_SIZE
                    converted_int = convert_int(data[i:i + BYTES_SIZE])

                idx_info = IdxInfo(precursorMass, seqOffset, seqLength, protein_ids)
                idx_info_list.append(idx_info)
                i += BYTES_SIZE

        return idx_info_list

    @staticmethod
    def serialize(idx_db: str, idx_info_list: [IdxInfo]):

        # TODO: Figure out why blob is separated by different idx files.
        # Why arbitrary cutoff for 1.idx.
        # Space requirements?
        # TODO: Output to SQLite file
        blob = []
        for idx_info in idx_info_list:
            blob.append(convert_float_to_bytes(idx_info.precursorMass))
            blob.append(convert_int_to_bytes(idx_info.seqOffset))
            blob.append(convert_int_to_bytes(idx_info.seqLength))
            for protein_id in idx_info.protein_ids:
                blob.append(convert_int_to_bytes(protein_id))
            blob.append(convert_int_to_bytes(END_INT_VALUE))
        pass