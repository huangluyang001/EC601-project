import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision.models as models
from torchsummary import summary
from preprocess import Preprocess
import sklearn

import torch.utils.data


class Pretrained_model:
    def adjusted_VGG(self):
        model = models.vgg11(pretrained=True)
        model.classifier[0] = torch.nn.Linear(in_features=25088, out_features=1024, bias=True)
        model.classifier[2] = torch.nn.Dropout(0.2)
        model.classifier[3] = torch.nn.Linear(in_features=1024, out_features=256, bias=True)
        model.classifier[5] = torch.nn.Dropout(0.2)
        model.classifier[6] = torch.nn.Linear(in_features=256, out_features=2, bias=True)
        for param in model.features.parameters():
            param.requires_grad = False
        #print(model)
        return model

class CNN_NET(nn.Module):
    def __init__(self, label_num, dropout_rate, in_channels=3):
        super(CNN_NET, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, 10, kernel_size=10)
        self.conv2 = nn.Conv2d(10, 10, kernel_size=10)
        self.conv2_drop = nn.Dropout2d(dropout_rate)
        self.linear1 = nn.Linear(24010,32)
        self.linear2 = nn.Linear(32, label_num)
        self.drop = dropout_rate

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 24010)
        x = F.relu(self.linear1(x))
        x = F.dropout(x, p=self.drop, training=False)
        x = self.linear2(x)
        return F.log_softmax(x, dim=1)

class FullConnection_NET(nn.Module):
    def __init__(self, label_num, dropout_rate):
        super(FullConnection_NET, self).__init__()
        self.linear1 = nn.Linear(150528, 512)
        self.linear2 = nn.Linear(512, 32)
        self.linear3 = nn.Linear(32, label_num)
        self.drop = dropout_rate
    def forward(self, x):
        x = x.view([-1,150528])
        x = F.relu(self.linear1(x))
        x = F.dropout(x, p=self.drop, training=True)
        x = self.linear2(x)
        x = F.dropout(x, p=self.drop, training=True)
        x = F.relu(self.linear3(x))
        return F.log_softmax(x, dim=1)


#https://pytorch.org/docs/stable/index.html
def train(model, device, train_loader, optimizer, epoch):
    model.train()
    for batch_idx, (x, y) in enumerate(train_loader):
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        x = x.float()
        y = y.long()
        output = model(x)
        loss = F.cross_entropy(output, y)
        loss.backward()
        optimizer.step()
        if (batch_idx+1) % epoch == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                batch_idx, batch_idx * len(x), len(train_loader.dataset),
                       100. * batch_idx / len(train_loader), loss.item()))

#https://pytorch.org/docs/stable/index.html
def test(model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for x, y in test_loader:
            x, y = x.to(device), y.to(device)
            x = x.float()
            y = y.long()
            output = model(x)
            test_loss += F.cross_entropy(output, y, reduction='sum').item()
            pred = output.max(1, keepdim=True)[1]
            correct += pred.eq(y.view_as(pred)).sum().item()
    test_loss /= len(test_loader.dataset)
    print('\nTest Set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))

def development(model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for x, y in test_loader:
            x, y = x.to(device), y.to(device)
            x = x.float()
            y = y.long()
            output = model(x)
            test_loss += F.cross_entropy(output, y, reduction='sum').item()
            pred = output.max(1, keepdim=True)[1]
            correct += pred.eq(y.view_as(pred)).sum().item()
    test_loss /= len(test_loader.dataset)
    print('\nDevelopment Set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))

def count_distribution(data_dict, sequence):
    train_count = {'0':0,'1':0}
    test_count = {'0': 0, '1': 0}
    dvlp_count = {'0': 0, '1': 0}
    train_sequence = sequence[0:550]
    test_sequence = sequence[640:]
    dvlp_sequence = sequence[550:640]
    label_list = data_dict['label'].tolist()
    for i in range(len(label_list)):
        if i in train_sequence:
            train_count[str(label_list[i])] += 1
        if i in dvlp_sequence:
            dvlp_count[str(label_list[i])] +=1
        if i in test_sequence:
            test_count[str(label_list[i])] += 1
    print('Train label count(0,1): '+str(train_count['0'])+','+str(train_count['1']))
    print('Test label count(0,1): ' + str(test_count['0']) + ',' + str(test_count['1']))
    print('Development label count(0,1): ' + str(dvlp_count['0']) + ',' + str(dvlp_count['1']))

if __name__ == '__main__':
    device = 'cuda'

    # Generating Dataset
    preprocessing = Preprocess()
    data = preprocessing.read_image()
    data['image'] = torch.from_numpy(data['image'])
    data['label'] = torch.from_numpy(data['label'])
    all_set = torch.utils.data.TensorDataset(data['image'],data['label'])
    np.random.seed(0)
    indices = np.random.randint(low=0, high=len(data['image']) - 1, size=len(data['image']))
    count_distribution(data_dict=data, sequence=list(indices))
    train_sequence = torch.from_numpy(indices[0:550])
    development_sequence = torch.from_numpy(indices[550:640])
    test_sequence =  torch.from_numpy(indices[640:])
    train_set = torch.utils.data.Subset(all_set, train_sequence)
    development_set = torch.utils.data.Subset(all_set, development_sequence)
    test_set = torch.utils.data.Subset(all_set, test_sequence)
    train_loader = torch.utils.data.DataLoader(dataset=train_set, batch_size=5, shuffle=True)
    test_loader = torch.utils.data.DataLoader(dataset=test_set, batch_size=1)
    dvlp_loader = torch.utils.data.DataLoader(dataset=development_set, batch_size=1)
    print('train_length:',len(train_set))
    print('development length',len(development_set))
    print('test_length:',len(test_set))


    # VGG13 part
    predefined = Pretrained_model()
    model = predefined.adjusted_VGG()
    model.cuda()
    summary(model,(3,224,224))

    try:
        model.load_state_dict(torch.load('VGG13.pth'))
    except FileNotFoundError:
        print('Initialization')
        optimizer = optim.Adam(model.parameters())
        for epoch in range(10):
            train(model, device, train_loader, optimizer, epoch=100)
            development(model, device, dvlp_loader)
            torch.save(model.state_dict(), 'VGG13.pth')
    print('Score of VGG13 with pretrained weight: ')
    test(model, device, test_loader)

    # CNN part
    model = CNN_NET(2, 0.2)
    model.cuda()
    summary(model,(3,224,224))

    try:
        model.load_state_dict(torch.load('CNN.pth'))
    except FileNotFoundError:
        print('Initialization')
        optimizer = optim.Adam(model.parameters())
        for epoch in range(20):
            train(model, device, train_loader, optimizer, epoch=100)
            development(model, device, dvlp_loader)
            torch.save(model.state_dict(), 'CNN.pth')

    print('Score of CNN before fine-tune: ')
    test(model, device, test_loader)
    # Fine tune
    model = CNN_NET(2, 0.5)
    model.cuda()
    try:
        model.load_state_dict(torch.load('CNN_finetune.pth'))
    except FileNotFoundError:
        print('Initialization')
        optimizer = optim.Adam(model.parameters(),lr=1e-4)
        for epoch in range(20):
            train(model, device, train_loader, optimizer, epoch=100)
            development(model, device, dvlp_loader)
            torch.save(model.state_dict(), 'CNN_finetune.pth')
    print('Score of CNN after fine-tune: ')
    test(model, device, test_loader)

    # only full-connection part
    model = FullConnection_NET(2, 0.2)
    model.cuda()
    summary(model,(3,224,224))

    try:
        model.load_state_dict(torch.load('full.pth'))
    except FileNotFoundError:
        print('Initialization')
        optimizer = optim.Adam(model.parameters())
        for epoch in range(20):
            train(model, device, train_loader, optimizer, epoch=100)
            development(model, device, dvlp_loader)
            torch.save(model.state_dict(), 'full.pth')

    print('Score of Full-connection before fine-tune: ')
    test(model, device, test_loader)
    # Fine tune
    model = CNN_NET(2, 0.5)
    model.cuda()
    try:
        model.load_state_dict(torch.load('full_finetune.pth'))
    except FileNotFoundError:
        print('Initialization')
        optimizer = optim.Adam(model.parameters(),lr=1e-4)
        for epoch in range(20):
            train(model, device, train_loader, optimizer, epoch=100)
            development(model, device, dvlp_loader)
            torch.save(model.state_dict(), 'full_finetune.pth')
    print('Score of Full-connection after fine-tune: ')
    test(model, device, test_loader)



