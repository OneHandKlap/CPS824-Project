config = {
    "BATCH_SIZE": 128,  # minibatch size
    "MEMORY_CAPACITY": 7000,  # replay memory
    "EPISODES_PER_EPOCH": 100,  # for training
    "NUMBER_OF_EPOCHS": 10,  # for training
    "FRAME_SKIP": 2,  # number of frames to skip per action
    "FRAME_STACK": 3,  # number of frames to stack
    "GAMMA": 0.999,  # discount factor
    "EPSILON": 1.0,  # exploration rate
    "EPSILON_MIN": 0.01,  # min epsilon
    "LEARNING_RATE": 0.001, #alpha learning rate initial
    "EPSILON_DECAY": 0.9999,  # rate at which epsilon decays
    "TARGET_UPDATE_INTERVAL": 10,  # interval at which to update target Q,
    "ACTION_SPACE": list({"turn_left": [-1, 1, .2], "turn_right": [1, 1, 0.2], "go": [0, 1, 0],"go_left": [-1, 1, 0], "go_right": [1, 1, 0], "brake": [0, 0, 0.2],"brake_left": [-1, 0, .2], "brake_right": [1, 0, 0.2]}.values())  # action space [direction, throttle, brake]
}
