import torch
from torch import nn
from .history_decoders import DirectDecoder

class Block(nn.Module):
    def __init__(self, width, hidden, scale):
        super().__init__()
        self.scale = scale
        self.layers = nn.Sequential(nn.LayerNorm(width), nn.Linear(width, hidden), nn.SiLU(), nn.Linear(hidden, width))
    def forward(self, h):
        return h + self.scale * self.layers(h)

class ReionizationHistoryEmulator(nn.Module):
    """Only output is decoded volume-mean global_xHI. No tau head."""
    def __init__(self, d_in, n_output, *, width=256, hidden=512, blocks=4, residual_scale=.5, decoder=None):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_in, width), nn.SiLU(),
            *[Block(width, hidden, residual_scale) for _ in range(blocks)], nn.LayerNorm(width), nn.Linear(width, n_output))
        self.decoder = decoder if decoder is not None else DirectDecoder()
        self.apply(self._init)
    @staticmethod
    def _init(m):
        if isinstance(m, nn.Linear):
            nn.init.xavier_uniform_(m.weight)
            nn.init.zeros_(m.bias)
    def forward(self, x, baseline=None):
        return self.decoder(self.net(x), baseline)
