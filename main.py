import random
import socket
import threading
import time
from dataclasses import dataclass


@dataclass
class Player:
    score: int = 0
    ready: bool = False


ADDRESS = ("localhost", 27015)

DURATION = 120
GRID_SIZE = 4


def handle_client(
    sock: socket.socket, player: Player, opponent: Player, board: str, words: set[str]
):
    guessed_words = set()

    sock.send(board.encode())

    sock.recv(1)
    player.ready = True
    while not opponent.ready:
        pass

    sock.send((0).to_bytes(1, byteorder="little"))

    start_time = time.time()
    current_time = time.time()

    while current_time - start_time < DURATION:
        sock.settimeout(DURATION - (current_time - start_time))

        try:
            word_length = int.from_bytes(sock.recv(4), byteorder="little")
        except TimeoutError:
            break

        word = sock.recv(word_length).decode()

        if word in words and word not in guessed_words:
            player.score += word_length
            guessed_words.add(word)
            sock.send((1).to_bytes(1, byteorder="little"))
        else:
            sock.send((0).to_bytes(1, byteorder="little"))

        current_time = time.time()

    sock.send((opponent.score).to_bytes(4, byteorder="little"))

    sock.close()


def main():
    boards: list[tuple[str, set[str]]] = []

    with open("boards.txt", "r") as file:
        board_line = 0

        for i, line in enumerate(file):
            if i == board_line:
                boards.append((line.removesuffix("\n"), set()))
            elif i == board_line + 1:
                board_line = board_line + int(line.removesuffix("\n")) + 2
            else:
                boards[len(boards) - 1][1].add(line.removesuffix("\n"))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    sock.bind(ADDRESS)
    sock.listen(10)

    pending_client = None

    while True:
        client, _ = sock.accept()

        if pending_client is not None:
            board, words = random.choice(boards)

            player_1 = Player()
            player_2 = Player()

            thread_1 = threading.Thread(
                target=handle_client, args=(client, player_1, player_2, board, words)
            )
            thread_1.start()

            thread_2 = threading.Thread(
                target=handle_client,
                args=(pending_client, player_2, player_1, board, words),
            )
            thread_2.start()

            pending_client = None
        else:
            pending_client = client


if __name__ == "__main__":
    main()
