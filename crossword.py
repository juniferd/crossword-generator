import sys
BLOCKS = {
    'black': u'\u2b1b',
    'white': u'\u2b1c',
}

class Crossword():
    def __init__(self, board_width, board_height, blocks=[], anchor_words=[]):
        self.board_width = board_width
        self.board_height = board_height
        self.blocks = self.generate_block_dict(blocks)
        self.anchor_words = self.generate_anchor_words_dict(anchor_words)
        self.board = self.generate_board()
        self.all_words = self.read_words()
        self.terminal_commands()

    def generate_anchor_words_dict(self, anchor_words):
        anchors = {}
        for word in anchor_words:
            start_pos = word[1]
            letters = list(word[0])
            direction = word[2]
            for i in range(len(letters)):
                if direction == 'across':
                    # increment x
                    anchors[(start_pos[0] + i, start_pos[1])] = letters[i]
                else:
                    # increment y
                    anchors[(start_pos[0], start_pos[1] + i)] = letters[i]
        return anchors

    def generate_block_dict(self, block_list):
        blocks = {}
        for block in block_list:

            blocks[block] = block
        return blocks

    def generate_board(self):
        width = range(0, self.board_width)
        height = range(0, self.board_height)
        # board_row = map(lambda x: x, width)
        # board = map(lambda y: board_row, height)
        board = []
        for y in height:
            row = []
            for x in width:
                if (x, y) in self.blocks:
                    row.append(BLOCKS['black'])
                elif (x, y) in self.anchor_words:
                    row.append(self.anchor_words[(x, y)].upper())
                else:
                    row.append(BLOCKS['white'])
            board.append(row)
        return board

    def read_words(self):
        # use system dictionary for words
        with open('/usr/share/dict/words') as f:
            words = [line.rstrip() for line in f]
        return words

    def pretty_print_board(self):
        # print board here
        for i in range(len(self.board)):
            row = self.board[i]
            print_row = ''
            for j in range(len(row)):
                print_row += row[j] + ' '
            print(print_row).encode('utf-8')

    def terminal_commands(self):
        self.pretty_print_board()
        while 1:
            print('where should i create a word? ("x, y")')
            res = raw_input()
            if res in ['Q', 'q', 'quit']: break
            self.find_word(res)

    def add_letter(self, letter):
        if letter == BLOCKS['white']:
            return str(' ')
        elif letter == BLOCKS['black']:
            return
        else:
            return letter

    def get_letters(self, start_pos, direction):
        # return list of letters currently on board
        x = start_pos[0]
        y = start_pos[1]
        letters = []
        # TODO make this less shitty
        if direction == 'across':
            for i in range(self.board_width - x):
                letter = self.board[y][x + i]
                if letter == BLOCKS['white']:
                    letters.append(str(' '))
                elif letter == BLOCKS['black']:
                    break
                else:
                    letters.append(letter)
        else:
            for i in range(self.board_height - y):
                letter = self.board[y + i][x]
                if letter == BLOCKS['white']:
                    letters.append(str(' '))
                elif letter == BLOCKS['black']:
                    break
                else:
                    letters.append(letter)
        return letters

    def add_new_word_to_board(self, new_word, position, direction):
        x = position[0]
        y = position[1]
        if direction == 'across':
            for i, letter in enumerate(new_word):
                self.board[y][x + i] = letter.upper()
        else:
            for i, letter in enumerate(new_word):
                self.board[y + i][x] = letter.upper()

    def find_word(self, coord_dir):
        coord_dir_list = coord_dir.split(',')
        coord = (int(coord_dir_list[0]), int(coord_dir_list[1]))
        # get all possible across and down suggestions
        print('pick a direction')
        pick_direction = raw_input()
        if pick_direction in ['across', 'a', 'A']:
            across = self.get_letters(coord, 'across')
            print(self.suggest_words(across))
            print('pick a word for across')
            new_across = raw_input()
            self.add_new_word_to_board(new_across, coord, 'across')
            self.pretty_print_board()
        elif pick_direction in ['down', 'd', 'D']:
            down = self.get_letters(coord, 'down')
            print(self.suggest_words(down))
            print('pick a word for down')
            new_down = raw_input()
            self.add_new_word_to_board(new_down, coord, 'down')
            self.pretty_print_board()
        else:
            return

    def get_start_of_word(self, position, direction):
        # if across decrement x until edge or black square
        # if down decrement y until edge or black square
        pass

    def suggest_words(self, restriction):
        suggested_words = []
        print('restrictions', restriction)
        for word in self.all_words:
            if len(word) == len(restriction):
                for i, letter in enumerate(restriction):
                    if letter != ' ' and letter.lower() != word[i].lower():
                        break
                    elif letter == ' ':
                        # check in other direction for all possible words
                        pass
                else:
                    suggested_words.append(word)
        return suggested_words

if __name__ == '__main__':
    black_squares = [
        (0, 0),
        (0, 1),
        (2, 1)
    ]
    anchor_words = [
        ('aloe', (0, 2), 'across')
    ]
    crossword = Crossword(4, 5, black_squares, anchor_words)
