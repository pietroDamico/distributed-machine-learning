import torch
import torchvision
from torch.utils.data import DataLoader, Subset
import torch.nn as nn
from sklearn.model_selection import train_test_split
import io
import torch.nn.functional as F
import json


EPOCHS = 1
LEARNING_RATE = 1e-2


def saveToIPFS(client, filePath):
	res = client.add(filePath)
	return res

def downloadFromIPFS(client, hashFile):
	return io.BytesIO(client.cat(hashFile))

class cnn(nn.Module):
	def __init__(self):
		super().__init__()
		self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)  # Assuming input_shape=(28, 28, 1)
		self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
		self.conv3 = nn.Conv2d(64, 64, kernel_size=3, padding=1)
		self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
		self.flatten = nn.Flatten()
		self.fc1 = nn.Linear(64 * 7 * 7, 100)  # Calculated from the output of the last MaxPooling layer
		self.fc2 = nn.Linear(100, 10)

	def forward(self, x):
		x = F.relu(self.conv1(x))
		x = self.pool(x)
		x = F.relu(self.conv2(x))
		x = F.relu(self.conv3(x))
		x = self.pool(x)
		x = self.flatten(x)
		x = F.relu(self.fc1(x))
		x = self.fc2(x)
		return F.log_softmax(x, dim=1)  # Using log_softmax for numerical stability

def getDevice():
	# Check for GPU availability
	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
	print(f"Using device: {device}")

def getDataLoaders(num_workers, batch_size=32, batch_size_test=256, train_test_ratio=0.8):
	transform = torchvision.transforms.Compose([
									torchvision.transforms.ToTensor(),
									torchvision.transforms.Normalize(
										(0.1307,), (0.3081,))
									])

	## MNIST dataset(images and labels)
	mnist_dataset = torchvision.datasets.MNIST(root = 'data/', download = True, train = True, transform = transform)

	# Calculate the size of each split
	split_size = len(mnist_dataset) // num_workers
	indices = torch.randperm(len(mnist_dataset)).tolist()
	worker_indices = [indices[i * split_size:(i + 1) * split_size] for i in range(num_workers)]

	# Function to split indices into train and test
	def train_test_split_indices(indices, train_size):
		train_indices, test_indices = train_test_split(indices, train_size=train_size)
		return train_indices, test_indices

	# Create a list of tuples (train_indices, test_indices) for each worker
	worker_train_test_indices = [train_test_split_indices(worker_idx, train_test_ratio) for worker_idx in worker_indices]

	# Create subsets for each worker
	worker_subsets = [(Subset(mnist_dataset, worker_train_test_indices[i][0]), 
					Subset(mnist_dataset, worker_train_test_indices[i][1])) for i in range(num_workers)]

	# Create dataloaders for each worker	
	worker_dataloaders = [(DataLoader(worker_subsets[i][0], batch_size=batch_size, shuffle=True), 
						DataLoader(worker_subsets[i][1], batch_size=batch_size_test, shuffle=False)) for i in range(num_workers)]
	
	return worker_dataloaders