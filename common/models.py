import torch.nn as nn
import torch.nn.functional as F
class FeedForwardNetwork(nn.Module):

    def __init__(self, layers_shapes, activations):
        nn.Module.__init__(self)
        self.activations = activations
        self.layers_shapes = layers_shapes
        for i in range(0, len(self.layers_shapes)):
            shape = self.layers_shapes[i]
            setattr(self, 'fc' + str(i), nn.Linear(shape[0], shape[1]))

    def forward(self, x):
        for i in range(0, len(self.layers_shapes)):
            x = getattr(self, 'fc' + str(i))(x)
            x = self.activations[i](x)
        return x

    def __str__(self):
        activations = ".".join([f.__name__ for f in self.activations])
        topology = ".".join([ str(layer[0]) + "_" + str(layer[1]) for layer in self.layers_shapes])
        return "FeedForwardNetwork_" + topology + '_' + activations
