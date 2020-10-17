import argparse
import haxball.async_common as async_common

from bots.bot_example import ChasingBot
from bots.behaviour_tree import BehaviourTree
from bots.strategy import Strategy

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", type=int, default=0, help="Different agents must be placed on different communication channels.")
    args = parser.parse_args()
    btree = BehaviourTree(str(args.channel));
    strategy = Strategy()

    btree.buildTree(strategy.getStrategy())
    try:
        async_common.run(btree.play())
    except KeyboardInterrupt:
        pass
