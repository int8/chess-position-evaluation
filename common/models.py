import torch.nn as nn
import torch.nn.functional as F


class FeedForwardNetwork(nn.Module):

    def __init__(self, layers_shapes, activations):
        super(Net, self).__init__()
        self.linear_layers = []
        self.activations = activations
        self.layers_shapes = layers_shapes

        for shape in self.layers_shapes:
            self.linear_layers.append(nn.Linear(shape[0], shape[1]))


    def forward(self, x):
        for i in range(0, len(self.linear_layers)):
            x = self.linear_layers[i](x)
            x = self.activations[i](x)
        return x
