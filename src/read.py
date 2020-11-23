
class Read:
    """
    This class represents the sequencing reads parsed from input files.
    For each read, we store its Id, actual sequence and the qualiry of 
    the read alongside the filename.
    """
    def __init__(self, filename, read_id, read_ptr, line, quality):
        self.filename = filename
        self.id = read_id
        self.read_ptr = read_ptr
        self.line = line
        self.quality = quality

    def kmers(self, k: int):
        for i in range(len(self.line) - k + 1):
            yield self.line[i:i+k]

    def __repr__(self) -> str:
        return "{}({}): {}\t {}\n\t\t\t\t{}".format(self.filename, self.read_ptr, self.id, self.line, self.quality)