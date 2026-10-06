import numpy as np

class Normalizer:
    """Stored log10 parameters stay in their existing coordinates."""
    def __init__(self, mean, scale):
        self.mean, self.scale = np.asarray(mean), np.asarray(scale)
        if not np.isfinite(self.mean).all() or not np.isfinite(self.scale).all() or np.any(self.scale <= 0):
            raise ValueError('Invalid normalization')

    @classmethod
    def fit(cls, x, *, split):
        if split != 'train':
            raise ValueError('Normalization may only fit train')
        x = np.asarray(x, float)
        if x.ndim != 2 or len(x) < 2 or not np.isfinite(x).all():
            raise ValueError('Invalid training inputs')
        sd = x.std(0)
        return cls(x.mean(0), np.where(sd > 0, sd, 1.0))

    def transform(self, x):
        return (np.asarray(x) - self.mean) / self.scale

    def as_dict(self):
        return {'mean': self.mean.tolist(), 'scale': self.scale.tolist()}

def logit(x, epsilon):
    if not 0 < epsilon < .5:
        raise ValueError('Invalid clipping epsilon')
    x = np.asarray(x)
    if not np.isfinite(x).all() or np.any((x < 0) | (x > 1)):
        raise ValueError('Invalid history before representation clipping')
    q = np.clip(x, epsilon, 1-epsilon)
    return np.log(q) - np.log1p(-q)

def fit_pca(values, k, *, split):
    if split != 'train':
        raise ValueError('PCA may only fit train')
    values = np.asarray(values, float)
    if values.ndim != 2 or not np.isfinite(values).all() or not 1 <= k <= min(values.shape):
        raise ValueError('Invalid PCA fit')
    mean = values.mean(0)
    _, _, vh = np.linalg.svd(values - mean, full_matrices=False)
    return mean, vh[:k]
