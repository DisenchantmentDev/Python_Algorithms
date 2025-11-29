def nQueensAll(n: int):
    if n < 4:
        raise ValueError
    def placeQueen(rank: int):
        # base case; append solution to answers we succesfully place all queens
        if rank == n:
            locationsCopy = list(queenLocations)
            answers.append(locationsCopy)
            return
        # nested inside of nQueensAll because of scope reasons
        # checking for each square in the current rank
        for column in range(n):
            # if the square we're on is a target of either positive or negative diagonals (or  just column) then we move to the next column
            if column in targetColumns or (rank + column) in targetDiagPos or (rank - column) in targetDiagNeg:
                continue
            queenLocations.add((rank, column)) # track position of queen
            targetColumns.add(column) # track column it targets
            targetDiagPos.add(rank + column) # track positive diagonal it targets
            targetDiagNeg.add(rank - column) # track negative diagonal it tarets
            placeQueen(rank + 1)
            queenLocations.remove((rank, column)) # remove tracking for queen and all her targeted squares
            targetColumns.remove(column)
            targetDiagPos.remove(rank + column)
            targetDiagNeg.remove(rank - column)
    max_val = (n * n) - 1
    queenLocations = set()
    targetColumns = set()
    targetDiagPos = set()
    targetDiagNeg = set()
    targetedSquares = set()
    answers = []
    placeQueen(0)
    return answers
