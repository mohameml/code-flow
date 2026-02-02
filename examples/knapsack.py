# knapsack.py

values = [3, 4, 5, 6]
weights = [2, 3, 4, 5]
W = 5

def knap(i, capacity):
    """
    i: index du dernier item considéré (0..n-1)
    capacity: capacité restante
    """
    if i < 0 or capacity == 0:
        return 0

    # ne pas prendre l'item i
    best = knap(i - 1, capacity)

    # prendre l'item i si possible
    if weights[i] <= capacity:
        best = max(best, values[i] + knap(i - 1, capacity - weights[i]))

    return best

n = len(values)
ans = knap(n - 1, W)
print("Knapsack naive =", ans)
