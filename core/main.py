import os
import sys
from core.args import parse_args, print_all_help
from core.commands.regminer4aprCheckout import checkout_command
from core.commands.regminer4aprCompile import compile_command
from core.commands.regminer4aprEnv import env_command
from core.commands.regminer4aprTest import test_command
from core.commands.regminer4aprInfo import info_command
from core.commands.regminer4aprClean import clean_command

def main():
    parser, subparsers, args = parse_args()
    
    if args.command is None or args.command == 'help':
        print_all_help(parser, subparsers)
    elif args.command == 'env':
        env_command()
    elif args.command == 'info':
        info_command(args.regressionbug_id)
    elif args.command == 'checkout':
        working_dir = args.working_dir if args.working_dir else os.getcwd()
        checkout_command(args.regressionbug_id, working_dir)
    elif args.command == 'compile':
        working_dir = args.working_dir if args.working_dir else os.getcwd()
        sys.exit(compile_command(working_dir))
    elif args.command == 'test':
        working_dir = args.working_dir if args.working_dir else os.getcwd()
        sys.exit(test_command(working_dir, args.test_case))
    elif args.command == 'clean':
        working_dir = args.working_dir if args.working_dir else os.getcwd()
        sys.exit(clean_command(working_dir))
