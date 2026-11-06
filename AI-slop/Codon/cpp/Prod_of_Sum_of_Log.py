from PSL import Prod_of_Sum_of_Log as _general, Prod_of_Sum_of_Log_test as _test


def Prod_of_Sum_of_Log(N: int) -> int:
    return _general(N, 3)


def Prod_of_Sum_of_Log_test(N: int) -> int:
    return _test(N, 3)
