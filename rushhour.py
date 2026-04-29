#!/usr/bin/env python3
import argparse
from verify import verify
from board import question, goal, move
from successors import successors
from search import solver

def main():
    parser = argparse.ArgumentParser(description="Rush Hour")
    sub = parser.add_subparsers(dest="action", required=True)

    pverify = sub.add_parser("verify")
    pverify.add_argument("-s", dest="level", required=True)

    pquestion = sub.add_parser("question")
    pquestion.add_argument("-s", dest="level", required=True)
    pquestion.add_argument("--whereis")
    pquestion.add_argument("--what")
    pquestion.add_argument("--size")
    pquestion.add_argument("--howmany", action="store_true")
    pquestion.add_argument("--goal", action="store_true")
    pquestion.add_argument("--move")

    psuccessors = sub.add_parser("successors")
    psuccessors.add_argument("-s", dest="level", required=True)

    psolver = sub.add_parser("solver")
    psolver.add_argument("-s", dest="level", required=True)
    psolver.add_argument("--strategy", required=True)
    psolver.add_argument("--depth", type=int)
    psolver.add_argument("--heuristic", type=int, default=0)
    psolver.add_argument("--stats", action="store_true")

    args = parser.parse_args()

    if args.action == "verify":
        print(verify(args.level))

    elif args.action == "question":
        if args.howmany:
            print(question(args.level, "--howmany"))
        elif args.size:
            print(question(args.level, "--size", args.size))
        elif args.whereis:
            print(question(args.level, "--whereis", args.whereis))
        elif args.what:
            print(question(args.level, "--what", args.what))
        elif args.goal:
            print("TRUE" if goal(args.level) else "FALSE")
        elif args.move:
            print(move(args.level, args.move))
        else:
            print("Error")

    elif args.action == "successors":
        for acc, est, cost in successors(args.level):
            print(f"[{acc},{est},{cost}]")

    elif args.action == "solver":
        solver(args.level, args.strategy, args.depth, args.stats, args.heuristic)

if __name__ == "__main__":
    main()
