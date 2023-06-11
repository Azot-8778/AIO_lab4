import numpy as np
import time

def open_case(fname):
    with open(fname, 'r') as f:
        n = int(f.readline())
        D = []
        for i in range(n):
            res = list(map(int, filter(lambda x: x.strip().isnumeric(), f.readline().split(' '))))
            D.append(res)
        f.readline()
        F = []
        for i in range(n):
            res = list(map(int, filter(lambda x: x.strip().isnumeric(), f.readline().split(' '))))
            F.append(res)

        D = np.array(D)
        F = np.array(F)

    return n, D, F

def calculate_score(phi, n, F, D):
    res = 0
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            
            res += F[i, j] * D[phi[i], phi[j]]

    return res

def calculate_delta(phi, r, s, n, F, D):
    res = 0
    for k in range(n):
        if k == r or k == s:
            continue
        res += (F[s, k] - F[r, k]) * (D[phi[s], phi[k]] - D[phi[r], phi[k]])

    return 2 * res

def local_search(n, F, D):
    #sol_init = {n: n for n in range(n)}
    sr = np.random.choice(n, size=n, replace=False)
    sol_init = {sr[idx]: idx for idx in range(n)}
    #sol_init_score = calculate_score(sol_init, n, F, D)
    phi = sol_init

    while True:
        first_improvement_found = False
        bits = [0 for i in range(n)]
        for f1 in range(n):
            for f2 in range(n):
                if f1 == f2: 
                    continue

                if bits[f2] == 1:
                    continue # dont look bits

                new_phi = phi.copy()
                new_phi[f1] = phi[f2]
                new_phi[f2] = phi[f1]

                delta = calculate_delta(new_phi, f1, f2, n, F, D)
                if delta < 0:
                    phi = new_phi
                    first_improvement_found = True
                    break
            
            if first_improvement_found:
                break
            else:
                bits[f1] = 1

        if not first_improvement_found:
            break

    return phi

fname = 'tai40a'
n, D, F = open_case(fname)
start = time.perf_counter()
l = local_search(n, F, D)
end = time.perf_counter()
ans = [-1 for i in range(n)]
for factory in l:
    ans[l[factory]] = factory + 1

print('time:', end-start)
print('answer:', ' '.join(map(str, ans)))
print('score:', calculate_score(l, n, F, D))

with open(f'{fname}.sol', 'w') as f:
    f.write(' '.join(map(str, ans)))