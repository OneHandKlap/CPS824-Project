from agents.dqn_agent import DQN_Agent
from config.adam_config import config


from models.dqn_deep import DQN_Deep
from models.dqn_deep2 import DQN_Deep2
from models.dqn_basic import DQN_Basic

import matplotlib.pyplot as plt
import torch
import psutil
import os
import numpy as np

from util.generate_video import generate_policy_video

from wrappers.memory_wrapper import MemoryWrapper

import gym

HEADLESS = False

if HEADLESS:
    from pyvirtualdisplay import Display
    display = Display(visible=0, size=(1400, 900))
    display.start()

    is_ipython = 'inline' in plt.get_backend()
    if is_ipython:
        from IPython import display

    plt.ion()

env = MemoryWrapper(lambda: gym.make("CarRacing-v0"))
agent = DQN_Agent(env, DQN_Deep2, config)


def memory_used():
    return psutil.Process(os.getpid()).memory_info().rss * 1e-6  # To megabyte


def memory_usage(agent, epoch, episode, ep_reward, ep_loss, epsilon, num_steps,lr):
    print(f"RAM: {memory_used()} - CUDA: {(100 - ((torch.cuda.memory_reserved(0) - torch.cuda.memory_allocated(0))/torch.cuda.memory_reserved(0) * 100))}%")
    '''
    plt.title('Ram over Time')
    plt.xlabel('Episodes')
    plt.ylabel('RAM')
    plt.scatter((epoch+1) * (episode+1), memory_used(), color="blue")
    plt.savefig("results/ram.png")
    '''


def log(agent, epoch, episode, ep_reward, ep_loss, epsilon, num_steps,lr):
    print(f"EPOCH: {epoch} - EPISODE: {episode} - REWARD: {ep_reward} - LOSS: {ep_loss} - EPSILON: {epsilon} - NUM_STEPS: {num_steps}")


fig1, (ax1) = plt.subplots(1, constrained_layout=True)
fig2, (ax2) = plt.subplots(1, constrained_layout=True)
fig3, (ax3) = plt.subplots(1, constrained_layout=True)
fig4, (ax4) = plt.subplots(1,constrained_layout=True)

rewards=[]
num_steps_acc=[]
loss=[]

def plot(agent, epoch, episode, ep_reward, ep_loss, epsilon, num_steps, lr):
    ax1.set_title('Rewards Over Episodes')
    ax1.set_xlabel('Episodes')
    ax1.set_ylabel('Rewards')
    ax1.scatter(((epoch-1) * 100) + episode, ep_reward, color="blue")
    rewards.append(ep_reward)

    ax2.set_title('Loss Over Episodes')
    ax2.set_xlabel('Episodes')
    ax2.set_ylabel('Loss')
    ax2.scatter(((epoch-1) * 100) + episode, ep_loss/num_steps, color="red")
    loss.append(ep_loss)

    ax3.set_title('Duration Over Episodes')
    ax3.set_ylabel('Duration')
    ax3.set_xlabel('Episodes')
    ax3.scatter((epoch * 100) + episode, num_steps, color="orange")
    num_steps_acc.append(num_steps)


    ax4.set_title('Learning Rate')
    ax4.set_ylabel('Duration')
    ax4.set_xlabel('Episodes')
    ax4.scatter((epoch * 100) + episode, lr, color="orange")

    fig1.savefig("results/plt1.png")
    fig2.savefig("results/plt2.png")
    fig3.savefig("results/plt3.png")
    fig4.savefig("results/plt4.png")


def save(agent, epoch, episode, ep_reward, ep_loss, epsilon, num_steps,lr):
    if episode % 100 == 0:
        print("SAVING AGENT")
        agent.save(f"results/rl_model_weights_{epoch}_{episode}.pth")
        generate_policy_video(agent, env, filename=f"results/video_{epoch}_{episode}")

        np.savetxt("data.txt",np.array([rewards,num_steps_acc,loss]))


agent.train(number_of_epochs=20,render=False, callbacks=[log, memory_usage, plot, save])
# agent.load("results/rl_model_weights_20_100.pth")
# generate_policy_video(agent, env, filename=f"tester")
