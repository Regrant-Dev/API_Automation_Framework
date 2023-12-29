import argparse
import json
import os
import subprocess

from helpers.file_transfer import handle_file_transfer, handle_file_transfer_cleanup


def update_environment_file(args):
    env = None
    with open(os.getcwd() + os.sep + 'environment.json', 'r+') as json_file:
        env = json.load(json_file)

        env['env'] = str(args.env).lower()

        if args.client_id is not None:
            env['client_id'] = args.client_id

        if args.client_secret is not None:
            env['client_secret'] = args.client_secret

        if args.base_url is not None:
            env['base_url'] = str(args.base_url).lower()

        if args.test_list is not None:
            env['test_list'] = args.test_list

        # Can be move or copy
        if args.transfer_method is not None:
            transfer_method = str(
                args.transfer_method).lower()
            if transfer_method != 'move' and transfer_method != 'copy':
                raise Exception(
                    "Transfer Method Invaid: Can only be move or copy")

            env['transfer_method'] = transfer_method

        json_file.seek(0)
        json.dump(env, json_file, indent=4)
        json_file.truncate()
        json_file.close()

    return env


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--env', required=True)
    parser.add_argument('--client_id')
    parser.add_argument('--client_secret')
    parser.add_argument('--base_url')
    parser.add_argument('--test_list', nargs='+')
    parser.add_argument('--transfer_method')

    known_args, unknown_args = parser.parse_known_args()

    env = update_environment_file(known_args)
    
    handle_file_transfer(env)

    pytest_args = ['pytest'] + unknown_args
    
    subprocess.run(pytest_args)
    
    handle_file_transfer_cleanup(env)

if __name__ == '__main__':
    main()