import argparse
import haxball.async_common as async_common
import sys

from bots.bot_example import ChasingBot
from bots.behaviour_tree import BehaviourTree
from bots.strategy import Strategy

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", type=int, default=0, help="Different agents must be placed on different communication channels.")
    parser.add_argument("--mode", type=str, default="hybrid", help="Bot's playing style ('defend', 'attack', or 'hybrid')")
    args = parser.parse_args()
    btree = BehaviourTree(str(args.channel));
    strategy = Strategy()

    if args.mode == "hybrid":
        btree.buildTree(strategy.getHybridStrategy())
    elif args.mode == "defend":
        btree.buildTree(strategy.getDefendStrategy())
    elif args.mode == "attack":
        btree.buildTree(strategy.getAttackStrategy())
    else:
        print("ERROR: Invalid bot playstyle. Choose one of 'defend', 'attack', or 'hybrid'.")
        sys.exit(1)

    try:
        async_common.run(btree.play())
    except KeyboardInterrupt:
        pass
