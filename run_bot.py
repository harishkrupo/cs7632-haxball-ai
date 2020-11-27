import argparse
import haxball.async_common as async_common
import sys

from bots.bot_example import ChasingBot
from bots.behaviour_tree import BehaviourTree
from bots.strategy import Strategy

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel", type=int, default=0, help="Different agents must be placed on different communication channels.")
    parser.add_argument("--mode", type=str, default="hybrid", help="Bot's playing style ('defend', 'attack', or, 'hybrid')")
    parser.add_argument("--difficulty", type=str, default="easy", help="Set the bot's difficulty ('easy', 'medium', or, 'hard')")
    args = parser.parse_args()
    modes = ['defend', 'attack', 'hybrid']
    difficulty = ['easy', 'medium', 'hard']

    if args.mode not in modes:
        print("modes must be one of: {}".format(modes))
    if args.difficulty not in difficulty:
        print("difficulty must be one of: {}".format(difficulty))

    btree = BehaviourTree(str(args.channel), args.difficulty);
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
