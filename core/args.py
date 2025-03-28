import argparse

from argparse import HelpFormatter
from operator import attrgetter

class SortingHelpFormatter(HelpFormatter):
    def add_arguments(self, actions):
        actions = sorted(actions, key=attrgetter("option_strings"))
        super(SortingHelpFormatter, self).add_arguments(actions)

def parse_args():
    parser = argparse.ArgumentParser(
        usage="regminer4apr <command> [<args>]",
        formatter_class=SortingHelpFormatter,
        add_help=False
    )
    
    subparsers = parser.add_subparsers(dest='command')

    # ==================== Help command =========================
    parser_help = subparsers.add_parser(
        'help', 
        description='show help message and exit', 
        usage='regminer4apr help',
        formatter_class=SortingHelpFormatter)

    # ==================== Env command =========================
    parser_env = subparsers.add_parser('env',
                                       description='display information about the system environment',
                                       usage='regminer4apr env',
                                       formatter_class=SortingHelpFormatter,
                                       add_help=False)

    # ==================== Info command =========================
    parser_info = subparsers.add_parser('info', 
                                        description='display information about a specific regression bug',
                                        usage='regminer4apr info -rb bug_id',
                                        formatter_class=SortingHelpFormatter,
                                        add_help=False)
    parser_info.add_argument('-rb', 
                             '--regressionbug_id',
                             required=True, 
                             help='regression bug ID to get information')

    # ==================== Checkout command ====================
    parser_checkout = subparsers.add_parser('checkout', 
                                            description='checkout a regression bug at a specific working directory',
                                            usage='regminer4apr check_out -rb bug_id -w working_dir',
                                            formatter_class=SortingHelpFormatter,
                                            add_help=False)
    parser_checkout.add_argument('-rb',
                                 '--regressionbug_id',
                                 required=True,
                                 help='regression bug ID to checkout')
    parser_checkout.add_argument('-w',
                                 '--working_dir',
                                 help='working directory to check out the bug')

    # ==================== Compile command ======================
    parser_compile = subparsers.add_parser('compile',
                                           description='compile source code at a specific working directory or current directory',
                                           usage='regminer4apr compile [-w working_dir]',
                                           formatter_class=SortingHelpFormatter,
                                           add_help=False)
    parser_compile.add_argument('-w', 
                                '--working_dir', 
                                help='working directory to compile [optional]')
    # ==================== Clean command ========================
    parser_clean = subparsers.add_parser('clean',
                                         description='clean compiled files at a specific working directory or current directory',
                                         usage='regminer4apr clean [-w working_dir]',
                                         formatter_class=SortingHelpFormatter,
                                         add_help=False)
    parser_clean.add_argument('-w',
                                '--working_dir',
                                help='working directory to clean [optional]')
    # ==================== Test command =========================
    parser_test = subparsers.add_parser('test',
                                        description='run all test cases at a specific working directory or current directory',
                                        usage='regminer4apr test [-w working_dir] [-t test_case]',
                                        formatter_class=SortingHelpFormatter,
                                        add_help=False)
    parser_test.add_argument('-w', 
                             '--working_dir', 
                             help='working directory to run tests [optional]')
    parser_test.add_argument('-t',
                             '--test_case',
                             help='specific test cases to run [optional]')

    return parser, subparsers, parser.parse_args()

def print_all_help(parser, subparsers):
    print("usage: " + parser.usage)
    print("\nCommands:")
    for choice in subparsers.choices:
        print(f"  {choice:<12} {subparsers.choices[choice].description}")