"""User-specified NNERO-style architectures for BT xHI; no WDM/native changes."""
import torch
from torch import nn

class Classifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.net=nn.Sequential(nn.Linear(10,30),nn.ReLU(),nn.Linear(30,30),nn.ReLU(),nn.Linear(30,1))
    def forward(self,x):return self.net(x).squeeze(-1)  # logits for BCEWithLogitsLoss

class PCAMLP(nn.Module):
    """PCA basis fixed from train positives; final loss is physical history MSE."""
    def __init__(self,mean,basis,*,transform='physical',epsilon=1e-6):
        super().__init__();k=basis.shape[0];layers=[];previous=10
        for _ in range(6):layers.extend([nn.Linear(previous,80),nn.ReLU()]);previous=80
        layers.append(nn.Linear(80,k));self.net=nn.Sequential(*layers)
        self.register_buffer('mean',torch.as_tensor(mean,dtype=torch.float32))
        self.register_buffer('basis',torch.as_tensor(basis,dtype=torch.float32))
        self.transform=transform;self.epsilon=epsilon
    def forward(self,x):
        history=self.mean+self.net(x)@self.basis
        return torch.sigmoid(history) if self.transform=='logit' else history
