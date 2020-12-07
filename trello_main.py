from trello import TrelloClient

client = TrelloClient(
    api_key='api-key',
    api_secret='api_secret'
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
    if board.name in ["Larissa tasks", "Tasks"]:
        move_all_tasks_in_todo(board)