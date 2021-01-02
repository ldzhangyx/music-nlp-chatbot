import torch
import torch.nn as nn

class LyricsGenerator(nn.module):
    def __init__(self):
        super().__init__()

    def input_encoder(self, input):
        pass

    def condition_encoder(self, condition):
        pass

    def forward(self, input, condition):
        pass