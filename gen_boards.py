import random
import string

GRID_SIZE = 4
MIN_WORDS = 75

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False


def solve_ruzzle(board: list[list[str]], dict_trie: TrieNode) -> set[str]:
    def dfs(node: TrieNode, prefix: str, i: int, j: int, visited: set[tuple[int, int]]):
        if node.is_word:
            words.add(prefix)

        for direction in DIRECTIONS:
            next_i, next_j = i + direction[0], j + direction[1]

            if (
                0 <= next_i < GRID_SIZE
                and 0 <= next_j < GRID_SIZE
                and (next_i, next_j) not in visited
                and board[next_i][next_j] in node.children
            ):
                dfs(
                    node.children[board[next_i][next_j]],
                    prefix + board[next_i][next_j],
                    next_i,
                    next_j,
                    visited | {(next_i, next_j)},
                )

    words = set()

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] in dict_trie.children:
                dfs(dict_trie.children[board[i][j]], board[i][j], i, j, {(i, j)})

    return words


def main():
    with open("dictionary.txt") as f:
        dictionary = set(f.read().splitlines())

    dict_trie = TrieNode()
    for word in dictionary:
        node = dict_trie
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode()
            node = node.children[letter]
        node.is_word = True

    boards = set()

    board_line = 0

    with open("boards.txt", "r") as file:
        for i, line in enumerate(file):
            if i == board_line:
                boards.add(line.removesuffix("\n"))
            if i == board_line + 1:
                board_line = board_line + int(line.removesuffix("\n")) + 2

    while True:
        words = set()

        while len(words) < MIN_WORDS:
            board = [
                [random.choice(string.ascii_uppercase) for _ in range(GRID_SIZE)]
                for _ in range(GRID_SIZE)
            ]

            words = solve_ruzzle(board, dict_trie)

        board_str = ""
        for row in board:
            for word in row:
                board_str += word

        if board_str in boards:
            continue

        boards.add(board_str)

        with open("boards.txt", "a") as file:
            file.write(board_str + "\n")
            file.write(str(len(words)) + "\n")
            for word in words:
                file.write(word + "\n")


if __name__ == "__main__":
    main()
