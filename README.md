# Fall 2023 blockchain project: decentralized machine learning

This is the project for the fall 2023 blockchain exam at Università di Roma - La Sapienza.

The goal is to train a shared model - a MNIST classifier - in a decentralized manner. 
Different workers with different datasets will participate in the training, which will be coordinated by a smart contract deployed on an Ethereum blockchain.

------
USAGE:

'cd' into the root folder.

'npx hardhat node' to spin up a local developement blockchain.

'npx hardhat run ./scripts/deploy.js --network localhost' to compile and deploy the smart contract. Edit deploy.js to set the number of rounds and the number of workers.

'python ./scripts/number_oracle.py' starts and oracle sending random numbers to the smart contract (they are needed for some stuff).

'python ./scripts/async_workers.py' starts the training task.

------

