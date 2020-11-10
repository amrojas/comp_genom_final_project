NUM_BUCKETS = 6500
FP_SIZE = 16
BUCKET_SIZE = 64
MAX_ITER = 500
## NOTE: let's make these configs obsolete. Modify the default config in the argument parser in main instead

class SketchConfig:
    def __init__(self, b=NUM_BUCKETS, f=FP_SIZE, s=BUCKET_SIZE, i=MAX_ITER, k=0, stash=0) -> None:
        self.k = k
        self.num_buckets = b
        self.fp_size = f
        self.bucket_size = s
        self.max_iter = i
        self.stash = stash