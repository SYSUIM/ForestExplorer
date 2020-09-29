import matplotlib
import torch
import torch.nn as nn
import numpy as np
import csv
import matplotlib.pyplot as plt
from torch.autograd import Variable
from matplotlib import cm

# Hyper Parameters
input_size = 78
output_size = 1
num_epochs = 1000000
lr = 0.000006
hidden_size = 78

# Toy Dataset
train_y = []
train_x = []

# Load input dataset
with open('./newshangshi_arr.txt', 'r', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    for line in reader:
        train_x.append(line)
train_x = np.array(train_x, dtype = 'float32')

# Load output dataset
with open('./2019shouru.csv', 'r', encoding = 'utf-8') as f:
    reader = csv.reader(f)
    for line in reader:
        train_y.append(line)
train_y = np.array(train_y, dtype = 'float32')
train_y = train_y.reshape(-1, 1)

# Linear Regression Model
class LinearRegression(nn.Module):
    def __init__(self, input_size, output_size, hidden_size):
        super(LinearRegression, self).__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out = self.linear1(x)
        out = self.linear2(out)
        return out

model = LinearRegression(input_size, output_size, hidden_size)

# Loss and Optimizer
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=lr)

# Train the Model
for epoch in range(num_epochs):
    inputs = Variable(torch.from_numpy(train_x))
    targets = Variable(torch.from_numpy(train_y))

    # Forward + Backward + Optimize
    optimizer.zero_grad()
    outputs = model(inputs)

    loss = criterion(outputs, targets)
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 100 == 0:
        print('Epoch [%d/%d], Loss: %.4f' % (epoch + 1, num_epochs, loss.item()))

# Save the Model
torch.save(model.state_dict(), 'model.pkl')