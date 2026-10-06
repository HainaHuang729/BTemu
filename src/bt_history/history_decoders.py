import torch
from torch import nn

class DirectDecoder(nn.Module):
    def forward(self, logits, baseline=None):
        return torch.sigmoid(logits)

class ResidualDecoder(nn.Module):
    def __init__(self, *, compatibility_passed, epsilon=1e-5, mean=None, basis=None, representation_passed=False):
        super().__init__()
        if not compatibility_passed:
            raise ValueError('PL compatibility gate has not passed')
        if not 0 < epsilon < .5:
            raise ValueError('Invalid epsilon')
        if (mean is None) != (basis is None):
            raise ValueError('PCA mean and basis must be supplied together')
        if basis is not None and not representation_passed:
            raise ValueError('PCA likelihood reconstruction gate has not passed')
        self.epsilon = epsilon
        self.register_buffer('mean', None if mean is None else torch.as_tensor(mean, dtype=torch.float32))
        self.register_buffer('basis', None if basis is None else torch.as_tensor(basis, dtype=torch.float32))

    def forward(self, output, baseline=None):
        if baseline is None or not torch.isfinite(baseline).all() or torch.any((baseline < 0) | (baseline > 1)):
            raise ValueError('Valid physical PL baseline required')
        residual = output if self.basis is None else self.mean + output @ self.basis
        return torch.sigmoid(torch.logit(baseline.clamp(self.epsilon, 1-self.epsilon)) + residual)
