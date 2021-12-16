from ai_base import ai_base
from turn import Turn

class HumanPlayer(ai_base):
    def __init__(self, color):
        super().__init__(color)

        # 0 --> command line / 1 --> ReactWeb Board
        self.input_mode = -1
        self.select_input_type()
        self.tg = -1
        self.no_avai_space = ['a1', 'a8', 'h1', 'h8']
        self.in_arg1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.in_arg2 = ['0', '1', '2', '3', '4', '5', '6', '7', '8']

    def select_input_type(self):
        input_type = 0
        # print("Options: \n 0) command-line-input (e.g. c1-c2) \n 1) React GUI (localhost:3000) \n")

        # while input_type not in [0, 1]:
        #     try:
        #         input_type = int(input("select 0/1."))
        #     except:
        #         print("That's not a valid option!")

        if int(input_type) == 0:
            self.input_mode = 0
        elif int(input_type) == 1:
            self.input_mode = 1


    def command_line_input(self):
        print("Please play your turn: (e.g.) c1-g6\n")
        while True:
            try:
                turn = input("input move:\t")
                if self.check_fen_input(turn):
                    x1 = ord(turn[0]) - ord('a')
                    y1 = ord(turn[1]) - ord('1')
                    # turn[2] ist '-'
                    x2 = ord(turn[3]) - ord('a')
                    y2 = ord(turn[4]) - ord('1')
                    return Turn(x1, y1, x2, y2)
                else:
                    raise Exception
            except:
                print("That's not a valid option!")

    def check_fen_input(self, input):
        input = input.split("-")
        if len(input) != 2:
            return False
        if len(input[0]) != 2 or len(input[1]) != 2:
            return False
        if input[0][0] not in self.in_arg1 or input[0][-1] not in self.in_arg2:
            return False
        if input[1][0] not in self.in_arg1 or input[1][-1] not in self.in_arg2:
            return False
        if input[0] in self.no_avai_space or input[1] in self.no_avai_space:
            return False
        return True


if __name__ == '__main__':
    h = HumanPlayer(0)
    h.input_mode = 0
    h.command_line_input()


