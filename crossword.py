import sys
BLOCKS = {
    'black': 'x',
    'white': '_',
}

class Crossword():
    def __init__(self, board_width, board_height, blocks=[], anchor_words=[]):
        self.stack = []
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
                print_row += row[j]
            print(print_row)

    def terminal_commands(self):
        self.pretty_print_board()
        while 1:
            print('where should i create a word? ("x, y")')
            res = raw_input()
            if res in ['u', 'undo', 'Q']:
                print "UNDOING LAST MOVE"
                if self.stack:
                    self.board = self.stack.pop()
                    self.pretty_print_board()

                continue

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

    def add_new_word_to_board(self, new_word, position, direction, tentative=True):
        x = position[0]
        y = position[1]
        self.stack.append([[r for r in row] for row in self.board])

        if direction == 'across':
            od = 'down'
            for i, letter in enumerate(new_word):
                self.board[y][x + i] = letter.upper()
                s = self.get_start_of_word([x+i, y], od)
                down = self.get_letters(s, 'down')
                if len(down) == 1 or not ' ' in down:
                    continue

                sugg = self.suggest_words(down, tentative)
                if not tentative:
                    print len(sugg), "POSSIBLE WORDS AT", s, "DOWN"

                if not sugg:
                    if not tentative:
                        print "NO WORDS AVAILABLE AT", s, ''.join(down)
                    self.board = self.stack.pop()
                    return
        else:
            od = 'across'
            for i, letter in enumerate(new_word):
                self.board[y + i][x] = letter.upper()
                s = self.get_start_of_word([x, y+i], od)
                across = self.get_letters(s, 'across')
                if len(across) == 1 or not ' ' in across:
                    continue

                sugg = self.suggest_words(across, tentative)
                if not tentative:
                    print len(sugg), "POSSIBLE WORDS AT", s, "ACROSS"
                if not sugg:
                    # print "NO WORDS AVAILABLE AT", s, ''.join(across)
                    self.board = self.stack.pop()
                    return

        return True

    def find_word(self, coord_dir):
        coord_dir_list = coord_dir.split(',')
        coord = (int(coord_dir_list[0]), int(coord_dir_list[1]))
        # get all possible across and down suggestions
        while True:
            print('pick a direction (down, across or back/quit)')
            pick_direction = raw_input()
            if pick_direction in ['across', 'a', 'A']:
                pick_direction = 'across'
                break
            elif pick_direction in ['down', 'd', 'D']:
                pick_direction = 'down'
                break
            elif pick_direction in ['back', 'b', 'quit', 'q']:
                return


        try:
            word = self.get_letters(coord, pick_direction)
        except:
            print "INVALID COORDINATES", coord, pick_direction
            return

        suggested = self.suggest_words(word)
        possible = []
        for w in suggested:
            added = self.add_new_word_to_board(w, coord, pick_direction)
            if added:
                possible.append(w)
                self.board = self.stack.pop()

        if not possible:
            print "NO POSSIBLE WORDS FOR", coord, pick_direction
            return

        print possible
        print 'pick a word for', pick_direction
        new_word = raw_input()
        self.add_new_word_to_board(new_word, coord, pick_direction, tentative=False)
        self.pretty_print_board()

    def get_start_of_word(self, position, direction):
        # if across decrement x until edge or black square
        # if down decrement y until edge or black square
        if direction == 'down':
            dx = 1
        else:
            dx = 0

        while position[dx] > 0:
            if self.board[position[1]][position[0]] == 'x':
                position[dx] += 1
                break
            position[dx] -= 1

        if self.board[position[1]][position[0]] == 'x':
            position[dx] += 1

        return position

    def suggest_words(self, restriction, at_least_one=False):
        suggested_words = []
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
                    if at_least_one:
                        return suggested_words

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
