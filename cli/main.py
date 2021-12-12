import argparse
import requests

my_parser = argparse.ArgumentParser()
my_parser.add_argument('command', metavar='C',
                       action='store', type=str)


command, params = my_parser.parse_known_args()

cli_params = {}

for i in range(0, len(params)-1, 2):
    cli_params[params[i].replace('--', '')] = params[i+1]

try:

    res = requests.get(f'http://localhost:5000/{command.command}',
                       data=cli_params
                       )

    if res.status_code == 404:
        res = requests.post(f'http://localhost:5000/{command.command}',
                            data=cli_params
                            )

    if res.status_code == 404:
        print('wrong command')
    else:

        print(res.text)

except:

    print('somithing gonna wrong')


