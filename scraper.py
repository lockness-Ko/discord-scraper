#! /usr/bin/env python3

import requests
import argparse
#import re
import json
import traceback


from time import sleep


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrapes discord channels")

    parser.add_argument("--amount", "-a", type=int, help="The number of messages you would like to scrape", default=50)
    parser.add_argument("--channel_id", "-c", type=int, help="The channel id for the channel you want to scrape", required=True)
    parser.add_argument("--token", "-t", type=str, help="The filepath where you have stored your token (just a plain text file with just your token is fine)", required=True)
    parser.add_argument("--grep", "-f", type=str, help="Return only messages that match this regex", default="[a-z0-9]")
    parser.add_argument("--attachments", type=bool, help="Include attachment urls in results", action=argparse.BooleanOptionalAction)
    parser.add_argument("--sort_reactions", "-R", type=bool, help="Sort messages by number of reactions", action=argparse.BooleanOptionalAction)

    args = parser.parse_args()

    token = open(args.token, "r").read().rstrip()

    headers = {
        "Authorization": token
    }

    MESSAGE_API_URL = f"https://discord.com/api/v9/channels/{args.channel_id}/messages?[Y]limit=[Z]"

    #pattern = re.compile(args.grep)

    if args.amount == 50:
        api_url = MESSAGE_API_URL.replace("[Y]", "").replace("[Z]", "50")

        out = requests.get(api_url, headers=headers).json()
        parsed_array = []

        for i in range(args.amount-1):
            try:
                #if not pattern.match(out[i]['content']):
                #    continue
                reactions = 0

                for reaction in range(len(out[i]['reactions'])):
                        reactions += out[i]['reactions'][reaction]['count']

                b = {
                    'id': out[i]['id'],
                    'username': out[i]['author']['username'],
                    'msg': out[i]['content'],
                    'attachments': out[i]['attachments'] if args.attachments else '',
                    'n_reactions': reactions
                }
                parsed_array.append(b)
            except Exception as e:
                pass
                #raise e
                #print(e)

    else:
        first = True
        last_id = ""
        parsed_array = []

        for i in range(int(args.amount/50)):
            print(f"[*] Getting page {i}")

            if first:
                api_url = MESSAGE_API_URL.replace("[Y]", "").replace("[Z]", "50")
                first = False
            else:
                api_url = MESSAGE_API_URL.replace("[Y]", f"before={last_id}&").replace("[Z]", "50")

            out = requests.get(api_url, headers=headers).json()

            for j in range(50):
                try:
                    if j == 49:
                        last_id = out[j]['id']

                    reactions = 0

                    for reaction in range(len(out[j]['reactions'])):
                            reactions += out[j]['reactions'][reaction]['count']

                    b = {
                        'id': out[j]['id'],
                        'username': out[j]['author']['username'],
                        'msg': out[j]['content'],
                        'attachments': out[i]['attachments'] if args.attachments else '',
                        'n_reactions': reactions
                    }
                    parsed_array.append(b)
                except Exception:
                    pass#print(traceback.format_exc())

            sleep(3)

    if args.sort_reactions:
        parsed_array = sorted(parsed_array, key=lambda x: x['n_reactions'], reverse=True)

    open("scraped.json", "w").write(json.dumps(parsed_array))
