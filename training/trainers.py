class ValueNetworkTrainer:

    def __init__(self, data_reader, model, loss_function, x_tensorize_f, y_tensorize_f, optimizer):
        self.data_reader = data_reader
        self.model = model
        self.loss_function = loss_function
        self.x_tensorize_f = x_tensorize_f
        self.y_tensorize_f = y_tensorize_f
        self.optimizer = optimizer

    def _train_single_epoch(self):

        for position in iter(self.data_reader):
            x = self.x_tensorize_f(position['X'])
            y = self.y_tensorize_f(position['Y'])
            self.optimizer.zero_grad()
            y_predicted = self.model(x)
            loss = self.loss_function(y_predicted, y)
            loss.backward()
            self.optimizer.step()

    def train(self, epochs = 5):
        self.model.train()
        for _ in range(0, epochs):
            self._train_single_epoch()
