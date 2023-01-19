from typing import List, Tuple, Iterable, Optional
import boggle_board_randomizer

# todo: erase import boggle_board_randomizer

Board = List[List[str]]
Path = List[Tuple[int, int]]


def get_location_string(location: Tuple[int, int], board: Board):
    y = location[0]
    x = location[1]
    return board[y][x]


def binary_search(word: str, words: List[str]) -> bool:
    """function that checks if a word is in words in O(logn) using binary
    search and returns True if it is in and False otherwise"""
    first_index = 0
    last_index = len(words) - 1
    while first_index <= last_index:
        middle_index = (first_index + last_index) // 2
        middle_word = words[middle_index]
        if word > middle_word:
            first_index = middle_index + 1
        elif word < middle_word:
            last_index = middle_index - 1
        # else: meaning the word equals to the middle word
        else:
            return True
    return False


def is_path_legal(path: Path, board: Board):
    """checks if a path is within the board boundaries and if every element of
    the path is linked to the last element"""
    location = path[0]
    last_y = location[0]
    last_x = location[1]
    height = len(board)
    width = len(board[0])
    for location in path[1:]:
        y = location[0]
        x = location[1]
        if y >= height or y < 0 or x >= width or x < 0:
            return False
        if abs(y - last_y) > 1 or abs(x - last_x) > 1 or \
                (y == last_y and x == last_x):
            return False
        last_y = y
        last_x = x
    return True


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[
    str]:
    if not is_path_legal(path, board):
        return None
    word_path = ""
    for location in path:
        location_str = get_location_string(location, board)
        word_path += location_str
    words_list = [word for word in words]  # create list from iterable
    if binary_search(word_path, words_list):
        return word_path
    return None


def get_valid_next_locations(location: Tuple[int, int], path: Path, height: int,
                             width: int) -> List[Tuple[int, int]]:
    y = location[0]
    x = location[1]
    next_locations = [(y + i, x + j) for j in range(-1, 2) for i in range(-1, 2)]
    next_locations.remove((y, x))
    if x == 0:
        next_locations.remove((y - 1, x - 1))
        next_locations.remove((y, x - 1))
        next_locations.remove((y + 1, x - 1))
    elif x == width - 1:
        next_locations.remove((y - 1, x + 1))
        next_locations.remove((y, x + 1))
        next_locations.remove((y + 1, x + 1))
    if y == 0:
        if (y - 1, x - 1) in next_locations: next_locations.remove(
            (y - 1, x - 1))
        if (y - 1, x) in next_locations: next_locations.remove((y - 1, x))
        if (y - 1, x + 1) in next_locations: next_locations.remove(
            (y - 1, x + 1))
    elif y == height - 1:
        if (y + 1, x - 1) in next_locations: next_locations.remove(
            (y + 1, x - 1))
        if (y + 1, x) in next_locations: next_locations.remove((y + 1, x))
        if (y + 1, x + 1) in next_locations: next_locations.remove(
            (y + 1, x + 1))
    # remove the locations that I already passed
    for path_loc in path:
        for next_loc in next_locations:
            if path_loc == next_loc:
                next_locations.remove(next_loc)
    return next_locations


def find_length_n_paths_helper(n: int, board: Board, words: Iterable[str],
                               loc: Tuple[int, int]) -> List[Path]:
    if n == 1:
        return [[(loc[0], loc[1])]]
    lst_to_return = []
    lst_next_loc = get_valid_next_locations(loc, (), len(board), len(
        board[0]))  # todo:add tupple later for checking if loc has been stept on
    for next_loc in lst_next_loc:
        next_paths = find_length_n_paths_helper(n - 1, board, words, next_loc)
        new_next_path = []
        for path in next_paths:
            new_next_path.append([loc] + path)
        lst_to_return.extend(new_next_path)
    return lst_to_return


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[
    Path]:
    n_paths = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            n_paths.extend(find_length_n_paths_helper(n, board, words, (i, j)))
    return n_paths


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[
    Path]:
    pass


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    pass


if __name__ == '__main__':
    pass
    f = open('boggle_dict.txt', 'r')
    words = f.read().split('\n')
    words.remove('')
    board = boggle_board_randomizer.randomize_board(boggle_board_randomizer.LETTERS)
    # board = [['O', 'T', 'H', 'S'],
    #          ['S', 'R', 'E', 'K'],
    #          ['T', 'B', 'QU', 'E'],
    #          ['P', 'E', 'A', 'R']]
    from pprint import pprint
    pprint(board)
    # print(is_valid_path(board, [(3, 0), (3, 1), (2, 0), (2,-1)], words))
    print(find_length_n_paths_helper(9,board,words, (2,2)))
