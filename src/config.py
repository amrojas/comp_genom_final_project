class SketchConfig:
    def __init__(self, b, f, s, i, k, stash, e, fp_prob, auto) -> None:
        self.k = k
        self.num_buckets = b
        self.fp_size = f
        self.bucket_size = s
        self.max_iter = i
        self.stash = stash
        self.expected_items = e
        self.fp_prob = fp_prob
        self.auto = auto