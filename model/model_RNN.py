import numpy as np
import torch
from torch import nn
from torch.autograd import Variable
import csv

# Hyper Parameters
# 批次，公司个数
batch_size = 228
# 时间长度
seq_len = 3
# 单个公司特征个数
input_size = 1552
# 隐层size
hidden_size = 1552
# RNN层数
num_layers = 1
# 学习率
learning_rate = 0.0000001
# 输出size
output_size = 1
# 训练循环次数
epoch_num = 100000

train_x_path = './228_newsSeq.txt'
train_y_path = './228_newsYSeq.txt'

# Load Train Data
train_x = np.loadtxt(train_x_path).reshape(228,3,-1).reshape(-1,1552).reshape(3,228,1552)
train_x = train_x.astype(np.float32)

# Load Fit Data
train_y = np.loadtxt(train_y_path).reshape(228*3).reshape(3,228,1)
train_y = train_y.astype(np.float32)

# RNN Model
class model_rnn(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, batch_size, num_layers):
        super(model_rnn, self).__init__()
        self.num_layers = num_layers
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.batch_size = batch_size
        self.rnn = torch.nn.RNN(input_size = self.input_size,
                               hidden_size = self.hidden_size,
                               num_layers = self.num_layers)
        self.fc = nn.Linear(hidden_size, output_size)
        
    def forward(self, inputs):
        hidden0 = torch.zeros(self.num_layers,
                             self.batch_size,
                             self.hidden_size).cuda()
        out, hidden = self.rnn(inputs, hidden0)
        fc_out = self.fc(out)
        return fc_out

# To CUDA
model_rnn = model_rnn(input_size, hidden_size, output_size, batch_size, num_layers)
model_rnn.cuda()

# Loss and Optimizer
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model_rnn.parameters(), lr = learning_rate)

# Train Model
for epoch in range(epoch_num):
    optimizer.zero_grad()
    inputs = Variable(torch.from_numpy(train_x)).cuda()
    targets = Variable(torch.from_numpy(train_y)).cuda()
    outputs = model_rnn(inputs)
    loss = criterion(outputs, targets.float())
    loss.backward()
    optimizer.step()
    
    if (epoch+1)%100 == 0: 
        print('Epoch [%d/%d], Loss: %.5f' 
               %(epoch+1, epoch_num, loss.item()))

# Save the Model
torch.save(model_rnn.state_dict(), 'RNN_model.pkl')