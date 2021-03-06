import copy
import time
# TODO
# 

board = []
pieces = {"0" : 0, 
          "WR" : 2, "WKt" : 3, "WB" : 4, "WQ" :  5, "WK" :  6, "WP" : 7,
          "BR" :-2, "BKt" :-3, "BB" :-4, "BQ" : -5, "BK" : -6, "BP" :-7}

piece_values = {
        "WR" : 5, "WKt" : 3, "WB" : 3, "WQ" :  9, "WK" : 999, "WP" : 1,
        "BR" :-5, "BKt" :-3, "BB" :-3, "BQ" : -9, "BK" :-999, "BP" :-1}

r_pieces = {}

WHITE = 1
BLACK = -1
MAX_DEPTH = 4

ENPASS = 41
P_2STEP = 42
KCASTLE_NO = 43
QCASTLE_NO = 44
CASTLE_NO = 45

KCASTLED = 46
QCASTLED = 47

def populate_board():
    p = pieces
    board = [[-1, -1,        -1,       -1,       -1,      -1,      -1,      -1,       -1,      -1,  -1, -1],
             [-1, -1,        -1,       -1,       -1,      -1,      -1,      -1,       -1,      -1,  -1, -1],
             [-1, -1,   p["WR"], p["WKt"],  p["WB"], p["WQ"], p["WK"], p["WB"], p["WKt"], p["WR"],  -1, -1],
             [-1, -1,   p["WP"],  p["WP"],  p["WP"], p["WP"], p["WP"], p["WP"], p["WP"],  p["WP"],  -1, -1],
             [-1, -1,   0      ,        0,        0,       0,       0,       0,        0,       0,  -1, -1],
             [-1, -1,   0      ,        0,        0,       0,       0,       0,        0,       0,  -1, -1],
             [-1, -1,   0      ,        0,        0,       0,       0,       0,        0,       0,  -1, -1],
             [-1, -1,   0      ,        0,        0,       0,       0,       0,        0,       0,  -1, -1],
             [-1, -1,   p["BP"],  p["BP"],  p["BP"], p["BP"], p["BP"], p["BP"], p["BP"],  p["BP"],  -1, -1],
             [-1, -1,   p["BR"], p["BKt"],  p["BB"], p["BQ"], p["BK"], p["BB"], p["BKt"], p["BR"],  -1, -1],
             [-1, -1,        -1,       -1,       -1,      -1,      -1,      -1,       -1,      -1,  -1, -1],
             [-1, -1,        -1,       -1,       -1,      -1,      -1,      -1,       -1,      -1,  -1, -1]]
              
    bt = [[i for i in range(12)] for j in range(12)]
    for i in range(12):
        for j in range(12):
            bt[i][j] = board[j][i]
    board = bt

    board.extend([[True, True], # Castling (queenside and kingside) flags for white
                  [True, True], # Castling flags for black
                  [-1, -1,     False,    False,    False,   False,   False,   False,    False,   False,  -1, -1],  # en-passant flags for white
                  [-1, -1,     False,    False,    False,   False,   False,   False,    False,   False,  -1, -1]]  # en-passant flags for black
                )

    return board

def dump_board(board):
    
    print 
    for j in range(9, 1, -1):
        print "%4d" % (j-1,),
        for i in range(2, 10):
            print "%4s" %r_pieces[board[i][j]],
        print ""

    for l in " ABCDEFGH":
        print "%4s" % l,
    print
    tf = {True : "True", False: "False"}
    print "White castle: Q: %s, K: %s" % (tf[board[-4][0]], tf[board[-4][1]])
    print "Black castle: Q: %s, K: %s" % (tf[board[-3][0]], tf[board[-3][1]])
    print 
    print "Enpassant white:"
    print board[-2][2:-2]
    print "Enpassant black:"
    print board[-1][2:-2]
    print 


def pawn_moves(colour, p, board):
    moves = []
    # Can I move forward?
    if board[p[0]][p[1] + colour] == 0:
        moves.append([p[0], p[1] + colour])
    for i in [1, -1]:
        # Can I take something?
        if board[p[0] + i][p[1] + colour] * colour < -2:
            moves.append([p[0] + i, p[1] + colour])

    if colour == WHITE:
        # If just starting out can move forward two squares
        if p[1] == 3 and board[p[0]][p[1] + 1] == 0 and board[p[0]][p[1] +2] == 0:
            moves.append([p[0], p[1] + 2, P_2STEP])

        # Can I take something en-passant?
        if p[1] == 5 + 1:
            for i in [1, -1]:
                if board[p[0] + i][p[1]] == -7 and board[-1][p[0] + i] == True:
                    moves.append([p[0] + i, p[1] + colour, ENPASS])
    else:
        if p[1] == 8 and board[p[0]][p[1] - 1] == 0 and board[p[0]][p[1] -2] == 0:
            moves.append([p[0], p[1] - 2, P_2STEP])


        # Can I take something en-passant?
        if p[1] == 4 + 1:
            for i in [1, -1]:
                print board[p[0] + i][p[1]]

                if board[p[0] + i][p[1]] == 7 and board[-2][p[0] + i] == True:
                    moves.append([p[0] + i, p[1] + colour, ENPASS])

    return moves

def rook_moves(colour, p, board):
    moves = []

    for k in (-1, 1):
        i = k
        while board[p[0]][p[1] + i] == 0:
            moves.append([p[0],p[1] + i])
            i += k
        if board[p[0]][p[1] + i] * colour < -2:
            moves.append([p[0],p[1] + i])


    for k in (-1, 1):
        i = k
        while board[p[0] + i][p[1]] == 0:
            moves.append([p[0] + i,p[1]])
            i += k
        if board[p[0] + i][p[1]] * colour < -2:
            moves.append([p[0] + i,p[1]])

    if colour == WHITE:
        if p[0] == 1 and p[1] == 1:
            # If q-side rook moves can no longer castle on this side
            for m in moves:
                m.append(QCASTLE_NO)
        if p[0] == 8 + 1 and p[1] == 1:
            for m in moves:
                m.append(KCASTLE_NO)
    else:
        if p[0] == 1 and p[1] == 8 + 1:
            for m in moves:
                m.append(QCASTLE_NO)
        if p[0] == 8 + 1 and p[1] == 8 + 1:
            for m in moves:
                m.append(KCASTLE_NO)

    return moves

def knight_moves(colour, p, board):
    moves = []

    for i, j in [(1,2), (2,1),
                 (1,-2), (2, -1),
                 (-1,-2), (-2, -1),
                 (-1,2), (-2, 1)]:
        if board[p[0] + i][p[1] + j] * colour < -2 or \
           board[p[0] + i][p[1] + j] == 0:
               moves.append([p[0] + i,p[1] + j])

    return moves

def bishop_moves(colour, p, board):
    moves = []

    for a, b in [(1,1), (1, -1), (-1, -1), (-1, 1)]:
        i, j = (a, b)
        while board[p[0] + i][p[1] + j] == 0:
            moves.append([p[0] + i,p[1] + j])
            i += a
            j += b
        if board[p[0] + i][p[1] + j] * colour < -2:
            moves.append([p[0] + i,p[1] + j])

    return moves

def queen_moves(colour, p, board):
    moves = []
    moves.extend(bishop_moves(colour, p, board))
    moves.extend(rook_moves(colour, p, board))
    return moves

def king_moves(colour, p, board):
    moves = []
    for i,j in [(1, 0), (1, 1), 
                (0, 1), (-1, 1),
                (-1, 0), (-1, -1),
                (0, -1), (1, -1)]:
        if board[p[0] + i][p[1] + j] * colour < -2 or \
           board[p[0] + i][p[1] + j] == 0:
               moves.append([p[0] + i,p[1] + j, CASTLE_NO])

    if colour == WHITE:
        if board[-4][0] == True: # queenside castling
            c_sq = [(5,2), (4,2)]
            if board[c_sq[0][0]][c_sq[0][1]] == 0 and board[c_sq[1][0]][c_sq[1][1]] == 0:
                attacked_sqs = attacked_squares(colour * -1, board)
                if not c_sq in attacked_sqs:
                    moves.append([c_sq[1][0], c_sq[1][1], QCASTLED, CASTLE_NO])
        if board[-4][1] == True: # kingside castling
            c_sq = [(7,2), (8,2)]
            if board[c_sq[0][0]][c_sq[0][1]] == 0 and board[c_sq[1][0]][c_sq[1][1]] == 0:
                attacked_sqs = attacked_squares(colour * -1, board)
                if not c_sq in attacked_sqs:
                    moves.append([c_sq[1][0], c_sq[1][1], KCASTLED, CASTLE_NO])
    if colour == BLACK:
        if board[-3][0] == True: # queenside castling
            c_sq = [(5,9), (4,9)]
            if board[c_sq[0][0]][c_sq[0][1]] == 0 and board[c_sq[1][0]][c_sq[1][1]] == 0:
                attacked_sqs = attacked_squares(colour * -1, board)
                if not c_sq in attacked_sqs:
                    moves.append([c_sq[1][0], c_sq[1][1], QCASTLED, CASTLE_NO])
        if board[-3][1] == True: # kingside castling
            c_sq = [(7,9), (8,9)]
            if board[c_sq[0][0]][c_sq[0][1]] == 0 and board[c_sq[1][0]][c_sq[1][1]] == 0:
                attacked_sqs = attacked_squares(colour * -1, board)
                if not c_sq in attacked_sqs:
                    moves.append([c_sq[1][0], c_sq[1][1], KCASTLED, CASTLE_NO])



    return moves

moves = {"WR"  : rook_moves}
moves = {"WR" : rook_moves, "WKt" : knight_moves, "WB" : bishop_moves,
         "WQ" : queen_moves, "WK" : king_moves, "WP" : pawn_moves,
         "BR" : rook_moves, "BKt" : knight_moves, "BB" : bishop_moves,
         "BQ" : queen_moves, "BK" : king_moves, "BP" : pawn_moves}



def m(square):
    row = "ABCDEFGH"
    pos = (row.find(square[0]), int(square[1]))
    return (pos[0] + 2, pos[1] + 1)

def mr(position):
    row = "ABCDEFGH"
    return "%s%d" % (row[position[0] - 2], position[1] -1)

def attacked_squares(colour, board):
    # n.b. this will be wrong for pawns
    all_moves = []
    for j in range(9, 1, -1):
        for i in range(2, 10):
            # If this square contains a
            # piece of the same colour
            # we are generating moves for
            if board[i][j] * colour >= 2:
                all_moves.append(m[0:2] for m in moves[r_pieces[board[i][j]]](colour, (i, j), board))
    return all_moves


def gen_moves(colour, board):
    boards = []
    board = [x[:] for x in board]
    # Reset en-passant flags for this move
    if colour == WHITE:
        board[-2] = [False,] * 12
    else:
        board[-1] = [False,] * 12
    for j in range(9, 1, -1):
        for i in range(2, 10):
            # If this square contains a
            # piece of the same colour
            # we are generating moves for
            if board[i][j] * colour >= 2:
                for m in moves[r_pieces[board[i][j]]](colour, (i, j), board):
                    new_board = [x[:] for x in board]
                    new_board[i][j] = 0

                    # If pawn is being taken en-passant remove the pawn 
                    # that has just been taken
                    if m[-1] == ENPASS:
                        new_board[m[0]][m[1] - colour] = 0
                    elif m[-1] == P_2STEP:
                        if colour == WHITE:
                            new_board[-2][m[0]] = True # set en-passant flag
                        else: 
                            new_board[-1][m[0]] = True # set en-passant flag

                    elif m[-1] == QCASTLE_NO:
                        if colour == WHITE:
                            new_board[-4][0] = False
                        else:
                            new_board[-3][0] = False
                    elif m[-1] == KCASTLE_NO:
                        if colour == WHITE:
                            new_board[-4][1] = False
                        else:
                            new_board[-3][1] = False
                    elif m[-1] == CASTLE_NO:
                        if colour == WHITE:
                            new_board[-4][0] = False
                            new_board[-4][1] = False
                        else:
                            new_board[-3][0] = False
                            new_board[-3][1] = False
                    if m[-2] == KCASTLED:
                        new_board[m[0] + 1][m[1]] = 0
                        new_board[m[0] - 1][m[1]] = pieces["WR"] * colour
                    elif m[-2] == QCASTLED:
                        new_board[m[0] - 2][m[1]] = 0
                        new_board[m[0] + 1][m[1]] = pieces["WR"] * colour



                    new_board[m[0]][m[1]] = board[i][j] 
                    move_string = r_pieces[board[i][j]] + " " +mr((m[0], m[1]))

                    boards.append((new_board, move_string))

    return boards

def evaluate(board):
    evaluation = 0
    for j in range(9, 1, -1):
        for i in range(2, 10):
            if not board[i][j] == 0:
                evaluation += piece_values[r_pieces[board[i][j]]]

    return evaluation

def play(colour, board, move_no, move_string = "", moves_ahead = 0):
    if moves_ahead == MAX_DEPTH:
        return (evaluate(board), board, move_string)
    new_move_no = move_no + moves_ahead
    moves_ahead += 1
    other_colour = colour * -1
    moves = []
    for m in gen_moves(colour, board):
        board = m[0]
        move = m[1]
        new_move_string = move_string
        if colour == WHITE:
            new_move_string += "%d: " % (new_move_no / 2 + 1) + move + ", "
        else:
            new_move_string += move + "\n"

        if moves_ahead == 1:
            j = list(play(other_colour, board, move_no, new_move_string, moves_ahead))
            j.append(board)
            moves.append(j)
        else:
            moves.append(play(other_colour, board, move_no, new_move_string, moves_ahead))

    if colour == WHITE:
        return max(moves, key = lambda i : i[0])
    else:
        return min(moves, key = lambda i : i[0])




for (k, v) in pieces.items():
    r_pieces[v] = k

board = populate_board()
dump_board(board)
# print evaluate(board)
b1 = board



colour = WHITE
move = 0
for i in range(100):
    print "Plie: %d" % i
    move += 1
    tick = time.time()
    e, b, s, b1 = play(colour,b1,move)
    tock = time.time()
    print "Time for move: %d" % (tock - tick)
    colour *= -1
    dump_board(b1)
    print s
    print 
