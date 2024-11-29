from trello import TrelloClient
import os
from dotenv import load_dotenv

def main():

    load_dotenv()

    client = TrelloClient(
        api_key=os.environ['TRELLO_API_KEY'],
        api_secret=os.environ['TRELLO_API_SECRET']
    )

    print("getting organizations list...", flush=True)
    org_list = client.list_organizations()
    family_boards = []
    for organization in org_list:
        if "family" in organization.name.lower():
            family_boards = organization.all_boards()
    print(f"loaded {len(family_boards)} boards", flush=True)


    def move_all_tasks_in_todo(board):
        board_lists = board.list_lists()

        target_list = None
        for list_ in board_lists:
            spaceless_name = list_.name.lower().replace(" ", "")
            if "todo" in spaceless_name:
                target_list = list_

        for list_ in board_lists:
            if list_ is not target_list:
                # Ability to ignore a list by starting a name with "_"
                if not list_.name.startswith("_"):
                    list_.move_all_cards(target_list)


    for board in family_boards:
        if "tasks" in board.name.lower():
            move_all_tasks_in_todo(board)


if __name__ == "__main__":
    main()
