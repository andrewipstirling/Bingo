from numpy import *
from collections import Counter
from multiprocessing import *


def new_board():
    cols = arange(1, 76).reshape(5, 15)
    return array([random.permutation(c)[:5] for c in cols])


def new_game():
    for token in random.permutation(arange(1, 76)):
        yield token


def winning(B):
    if ((B.sum(axis=0) == 5).any()):
        if ((B.sum(axis=1) == 5).any() or (trace(B) == 5 or trace(B.T) == 5)):
            return True

    if ((B.sum(axis=1) == 5).any()):
        if ((B.sum(axis=0) == 5).any() or (trace(B) == 5 or trace(B.T) == 5)):
            return True

    if (trace(B) == 5 or trace(B.T) == 5):
        if ((B.sum(axis=0) == 5).any() or (B.sum(axis=1) == 5).any()):
            return True

    """
    if B.sum()==25:
        return True  ## blackout
    """
    return False


def game_length(board, game):
    B = zeros((5, 5), dtype=bool)
    B[2, 2] = True
    for n, idx in enumerate(game, 1):
        B[board == idx] = True
        if winning(B):
            return n


def simulation(trials):
    C = Counter()
    b = new_board()
    for _ in range(trials):
        C[game_length(b, new_game())] += 1
    return C


if __name__ == '__main__':
    repeats = 10 ** 2
    trials = 10 ** 2
    numBoards = 200

    P = Pool()
    sol = sum(P.map(simulation, [trials, ] * repeats))
    P.close()
    P.join()

    X = array(sorted(filter(None, sol.keys())))
    Y = array([sol[x] for x in X])
    cumY = cumsum(Y)
    probnotwon1board = [(float(repeats * trials - y) / (repeats * trials)) for y in cumY]
    probnotwonanyboard = [x ** numBoards for x in probnotwon1board]
    probsomeboardwon = [1 - x for x in probnotwonanyboard]

    print("Number of boards: ", numBoards)
    print()
    print("Ball  Winners Cumulative  Prob 1 Board    Prob No   Prob Some")
    print("               Winners      Not Won      Board Won  Board Won")
    print()
    for i in range(len(X)):
        print(" {0:2d}   {1:6d}   {2:6d}       {3:1.6f}     {4:1.6f}    {5:1.6f} ".format(X[i], Y[i], cumY[i],
                                                                                          probnotwon1board[i],
                                                                                          probnotwonanyboard[i],
                                                                                          probsomeboardwon[i]))
    print()
