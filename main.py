from run import run

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--checksum',
        help='The checksum of the previous SDE.',
        required=True,
        dest='prev_checksum',
    )
    parser.add_argument(
        '-g',
        '--generator-group',
        help='The name of a generator group.',
        required=True,
        dest='generator_groups',
        action='append',
    )
    parser.add_argument(
        '-d',
        '--debug',
        help='Use the current directory as the SDE.',
        action='store_true',
        dest='debug',
    )
    args = parser.parse_args()
    prev_checksum = args.prev_checksum
    generator_groups = args.generator_groups
    try:
        debug = args.debug
    except AttributeError:
        debug = False

    new_checksum = run(prev_checksum, generator_groups, debug)
    if new_checksum is not None:
        print(new_checksum)

if __name__ == '__main__':
    main()
