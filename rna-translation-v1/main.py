import sys
from codons import CODONS



def check_file(file: list) -> str:
    if file[2:]:
        print(f"Usage: python {sys.argv[0]} <file>")
        sys.exit(0)
    return file[1]

def translation(data_rna: str) -> list:
    print(len(data_rna))
    if len(data_rna) % 3 != 0:
        print("Error: Incomplete terminal codon detected. Expected an intact coding sequence.")

    proteins: list = []

    for i in range(0, len(data_rna), 3):
        if not CODONS.get(data_rna[i:i+3], False):
            print(f"Warning: Unrecognized codon '{data_rna[i:i+3]}', substituted with 'X'.")
            proteins.append("X")
            continue
        elif data_rna[i:i+3] in {"UAA", "UAG", "UGA"}:
            yield proteins
            print(f"\033[1m\033[32mInfo: Stop codon ({data_rna[i:i+3]}) detected; starting a new polypeptide chain.\033[0m")
            proteins = []
            continue

        proteins.append(CODONS.get(data_rna[i:i+3]))

    yield proteins
        



def main() -> int:
    file: str = check_file(sys.argv)

    try:
        with open(file, "r") as data:

            endFile: bool = False
            gen = translation(data.read().strip().upper())

            while not endFile:
                proteins = next(gen, False)
                if not proteins:
                    endFile = True
                    break
                print("Peptide sequence: ", "-".join(proteins))


    except (FileNotFoundError, PermissionError) as error:
        print(error)

if __name__ == "__main__":
    main()
