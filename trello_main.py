import os
import json

import trello
from trello import TrelloClient
from dotenv import load_dotenv


load_dotenv()

def patched_fetch_json(self,
                       uri_path,
                       http_method='GET',
                       headers=None,
                       query_params=None,
                       post_args=None,
                       files=None):
    """ Fetch some JSON from Trello """

    # explicit values here to avoid mutable default values
    if headers is None:
        headers = {}
    if query_params is None:
        query_params = {}
    if post_args is None:
        post_args = {}

    # if files specified, we don't want any data
    data = None
    if files is None and post_args != {}:
        data = json.dumps(post_args)

    # set content type and accept headers to handle JSON
    if http_method in ("POST", "PUT", "DELETE") and not files:
        headers['Content-Type'] = 'application/json; charset=utf-8'

    headers['Accept'] = 'application/json'

    # construct the full URL without query parameters
    if uri_path[0] == '/':
        uri_path = uri_path[1:]
    url = 'https://api.trello.com/1/%s' % uri_path

    if self.oauth is None:
        query_params['key'] = self.api_key
        query_params['token'] = self.api_secret

    # perform the HTTP requests, if possible uses OAuth authentication
    response = self.http_service.request(http_method, url, params=query_params,
                                            headers=headers, data=data,
                                            auth=self.oauth, files=files,
                                            proxies=self.proxies)

    if response.status_code == 401:
        raise trello.Unauthorized("%s at %s" % (response.text, url), response)
    if response.status_code != 200:
        raise trello.ResourceUnavailable("%s at %s" % (response.text, url), response)

    return response.json()

TrelloClient.fetch_json = patched_fetch_json


client = TrelloClient(
    api_key=os.environ['TRELLO_API_KEY'],
    api_secret=os.environ['TRELLO_API_SECRET']
)

org_list = client.list_organizations()
for organization in org_list:
    if "family" in organization.name.lower():
        family_boards = organization.all_boards()


def move_all_tasks_in_todo(board):
    board_lists = board.list_lists()

    for list_ in board_lists:
        spaceless_name = list_.name.lower().replace(" ", "")
        if "todo" in spaceless_name:
            target_list = list_

    for list_ in board_lists:
        if list_ is not target_list:
            list_.move_all_cards(target_list)


for board in family_boards:
    if "tasks" in board.name.lower():
        move_all_tasks_in_todo(board)
