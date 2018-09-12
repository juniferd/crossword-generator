import sys
import time

BLOCKS = {
    'black': '#',
    'white': '_',
}
def turn_into_integers(arr):
    return map(lambda x: int(x), arr)

def terminal_commands():
    print('how big is this board? ("width, height")')
    (width, height) = turn_into_integers(raw_input().split(','))
    print('where would you like to place your black squares? ("x, y")')
    black_squares = []
    while 1:
        black_square = raw_input()
        if black_square in ['', 'stop', '\n']: break
        black_squares.append(tuple(turn_into_integers(black_square.split(','))))
        print('add another or press enter to stop adding black squares')

    print('where would you like to place anchor words? ("word, x, y, direction")')
    anchors = []
    while 1:
        anchor = raw_input()
        if anchor in ['', 'stop', '\n']: break
        anchor_list = anchor.split(',')
        anchor_pos = tuple(turn_into_integers([anchor_list[1], anchor_list[2]]))
        anchors.append(tuple([anchor_list[0], anchor_pos, anchor_list[3]]))
        print('add another or press enter to stop adding anchors')

    crossword = Crossword(width, height, black_squares, anchors)
    crossword.pretty_print_board()

    while 1:
        print('where should i create a word? ("x, y")')
        res = raw_input()
        if res in ['u', 'undo', 'Q']:
            print "UNDOING LAST MOVE"
            if crossword.stack:
                crossword.board = crossword.stack.pop()
                crossword.pretty_print_board()
                crossword.print_start_squares()

            continue

        if res in ['Q', 'q', 'quit']: break
        crossword.find_word(res)

class Crossword():
    __prepared__ = False
    dictionary = {}
    word_lookup = [{} for i in xrange(50)]
    words_of_size = [[] for i in xrange(50)]

    @classmethod
    def read_words(self):
        # use system dictionary for words
        with open('/usr/share/dict/words') as f:
            words = [line.rstrip() for line in f]
        return words

    @classmethod
    def prepare_words(self):
        if self.__prepared__:
            return

        self.all_words = self.read_words()
        self.__prepared__ = True
        # word_lookup[length][index][letter] = all words of size length with letter in position index
        start = time.time()
        for word in self.all_words:
            self.words_of_size[len(word)].append(word)
            self.dictionary[word.lower()] = True

            table = self.word_lookup[len(word)]
            for i in xrange(len(word)):
                k = word[i].lower()

                if not i in table:
                    table[i] = {}

                if not k in table[i]:
                    table[i][k] = []

                table[i][k].append(word)

        for table in self.word_lookup:
            for i in table:
                for k in table[i]:
                    table[i][k] = set(table[i][k])

        end = time.time()

        print "MAKING WORDS TOOK", end - start

    def __init__(self, board_width=10, board_height=10, blocks=[], anchor_words=[]):
        self.stack = []
        self.board_width = board_width
        self.board_height = board_height
        self.blocks = self.generate_block_dict(blocks)
        self.anchor_words = self.generate_anchor_words_dict(anchor_words)
        self.board = self.generate_board()
        self.all_words = self.read_words()
        self.prepare_words()


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

    def print_start_squares(self):
        checked = {}
        for x in xrange(self.board_width):
            for y in xrange(self.board_height):
                if self.board[y][x] == 'X':
                    continue

                for d in ['across', 'down']:
                    s = self.get_start_of_word([x, y], d)
                    sk = "%s,%s,%s" % (s[0], s[1], d)
                    if not sk in checked:
                        word = self.get_letters(s, d)
                        if len(word) <= 1:
                            continue

                        w = ''.join(word).lower()
                        sugg = []
                        if not ' ' in word:
                            if w in self.dictionary:
                                sugg = [w]
                        else:
                            checked[sk] = 1
                            sugg = self.suggest_words(word)
                            print len(sugg), "WORDS AT", s, d

                        if len(sugg) == 0:
                            print "INVALID WORD AT", s, w, ", UNDOING MOVE"
                            self.board = self.stack.pop()
                            self.pretty_print_board()

    def pretty_print_board(self):
        # print board here
        for i in range(len(self.board)):
            row = self.board[i]
            print_row = ''
            for j in range(len(row)):
                print_row += row[j]
            print(print_row)


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
        self.stack.append([[r for r in row] for row in self.board])

        if direction == 'across':
            od = 'down'
            for i, letter in enumerate(new_word):
                self.board[y][x + i] = letter.upper()
                s = self.get_start_of_word([x+i, y], od)
                down = self.get_letters(s, 'down')
                if len(down) == 1 or not ' ' in down:
                    continue

                sugg = self.suggest_words(down)
                if not sugg:
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

                sugg = self.suggest_words(across)
                if not sugg:
                    # print "NO WORDS AVAILABLE AT", s, ''.join(across)
                    self.board = self.stack.pop()
                    return

        return True

    def find_word(self, coord_dir):
        try:
            coord_dir_list = coord_dir.split(',')
            coord = (int(coord_dir_list[0]), int(coord_dir_list[1]))
        except ValueError, e:
            print e
            return
        except IndexError, e:
            print e
            return
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

        print "FINDING SUGGESTIONS", word
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

        print "FILTERED ", len(suggested), "TO", len(possible)
        print possible
        print 'pick a word for', pick_direction
        new_word = raw_input()
        self.add_new_word_to_board(new_word, coord, pick_direction)

        self.pretty_print_board()
        self.print_start_squares()

    def get_start_of_word(self, position, direction):
        # if across decrement x until edge or black square
        # if down decrement y until edge or black square
        if direction == 'down':
            dx = 1
        else:
            dx = 0

        while position[dx] > 0:
            if self.board[position[1]][position[0]] == '#':
                position[dx] += 1
                break
            position[dx] -= 1

        if position[1] < self.board_height and position[0] < self.board_width:
            if self.board[position[1]][position[0]] == '#':
                position[dx] += 1

        return position

    def suggest_words(self, restriction):
        suggested_words = []
        word_table = self.word_lookup[len(restriction)]
        sets = []
        has_letter = False
        for i, letter in enumerate(restriction):
            if letter.strip() != '':
                has_letter = True
                try:
                    sets.append(word_table[i][letter.lower()])
                except Exception, e:
                    print e
                    continue

        if not has_letter:
            # word must be blank?
            return [w for w in self.words_of_size[len(restriction)]]

        if sets:
            ret = set([s for s in sets[0]])
            for s in sets:
                ret = ret.intersection(s)

            return ret

        return []

if __name__ == '__main__':
    # black_squares = [
    #     (0, 0),
    #     (0, 1),
    #     (2, 1)
    # ]
    # anchor_words = [
    #     ('aloe', (0, 2), 'across')
    # ]
    # crossword = Crossword(4, 5, black_squares, anchor_words)
    # crossword.terminal_commands()
    terminal_commands()

