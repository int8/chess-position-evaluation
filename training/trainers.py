import torch
class ValueNetworkTrainer:

    def __init__(self, training_data_reader, model, loss_function, x_tensorize_f, y_tensorize_f, optimizer, use_cuda = True):
        self.training_data_reader = training_data_reader
        self.model = model
        self.loss_function = loss_function
        self.x_tensorize_f = x_tensorize_f
        self.y_tensorize_f = y_tensorize_f
        self.optimizer = optimizer
        self.use_cuda = use_cuda

        if self.use_cuda:
            self.model.cuda()

    def train_single_epoch(self):
        for position in iter(self.training_data_reader):
            if self.use_cuda:
                position['X'] = position['X'].cuda()
                position['Y'] = position['Y'].cuda()
            x = self.x_tensorize_f(position['X'])
            y = self.y_tensorize_f(position['Y'])
            self.optimizer.zero_grad()
            y_predicted = self.model(x)
            loss = self.loss_function(y_predicted, y)
            loss.backward()
            self.optimizer.step()

    def evaluate(self, data_reader, evaluation_metric):
        sum_metric = 0.0
        counter = 0.
        for position in iter(data_reader):
            x = self.x_tensorize_f(position['X'])
            y = self.y_tensorize_f(position['Y'])
            y_predicted = self.model(x)
            sum_metric += evaluation_metric(y, y_predicted, self.loss_function)
            counter += 1.
        return sum_metric / counter

    def save_model_state(self, prefix = 'final_', output_dir = '.'):
        torch.save(self.model.state_dict(), output_dir + '/' + prefix +  str(self.model) + '.model')

    def load_model_state(self, model_state_file):
        self.model.load_state_dict(
            torch.load(model_state_file)
        )
