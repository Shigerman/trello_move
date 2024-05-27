# trello_move

![logo](https://github.com/Shigerman/trello_move/raw/main/trello.jpg)

A script which helps to automate activities with my Trello boards.

### instruments used
* Python for backend
* Poetry for virtual environment
* Raspberry Pi for a server

### activity algorithm
Find all the cards in my "doing" and "done" daily-routines-Trello-boards >>>
move all the cards to "todo" every day at 6 am.

### install
```sh
python3 - poetry install
ln -s -f /home/user/trello/trello.service /etc/systemd/system/trello.service
ln -s -f /home/user/trello/trello.timer /etc/systemd/system/trello.timer
echo TRELLO_API_KEY=foo > /home/user/trello/.env
echo TRELLO_API_SECRET=bar >> /home/user/trello/.env
```
