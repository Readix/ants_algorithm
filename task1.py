import numpy as np

# Константы
cQ = 1e11
cA = 1
cB = 2

ants_quan = 2000  # Количество муравьев
pher_speed = 0.03  # Скорость испарения фермента
len_regular_coef = 8

def len_regular(len):
    return len ** len_regular_coef


def reset_pher_matrix():
    for i in range(quan_vers):
        for j in range(quan_vers):
            pher_matrix[i][j] = 1.0 * np.random.randint(1, 4)


def get_relevance(ver1, ver2):
    """
    Возвращает (Tij**A)/(Lij**B), где
    i, j = ver1, ver2
    """
    return (pher_matrix[ver1][ver2] ** cA) / (len_matrix[ver1][ver2] ** cB)


def get_vertex(cur_ver, past_vers):
    """
    Выбирает следующую вершину для прохода
    :param cur_ver: текущая вепшина
    :param past_vers: пройденные вершины
    :return: следующая вершина
    """
    gen_sum = 0
    for tmp_ver in range(quan_vers):
        if past_vers.count(tmp_ver) > 0:
            continue
        gen_sum += get_relevance(cur_ver, tmp_ver)

    prob = {}
    p_sum = 0

    for tmp_ver in range(quan_vers):
        if past_vers.count(tmp_ver) > 0:
            continue
        p_sum += 100 * get_relevance(cur_ver, tmp_ver) / gen_sum
        prob[tmp_ver] = p_sum

    rand = np.random.randint(1, 100000)/1000.0
    for key in prob.keys():
        if rand < prob[key]:
            return key

    print("error")
    return -1


def ant_cycle():
    """
    Имитирует проход одного муравья
    :return: длина пути и пройденные вершины
    """
    way_len, t = [0, 0]
    past_vers = []
    start_ver = np.random.randint(0, quan_vers)
    cur_ver = start_ver
    past_vers.append(cur_ver)
    while len(past_vers) < quan_vers:
        next_ver = get_vertex(cur_ver, past_vers)

        way_len += len_matrix[cur_ver][next_ver]
        cur_ver = next_ver
        past_vers.append(cur_ver)

    past_vers.append(start_ver)
    way_len += len_matrix[cur_ver][start_ver]

    return [way_len, past_vers]


def greedy_ant():
    """
    Имитирует проход жадного по феромонам муравья
    :return: длина пути и пройденные вершины
    """
    way_len, t = [0, 0]
    past_vers = []
    start_ver = np.random.randint(0, quan_vers)
    cur_ver = start_ver
    past_vers.append(cur_ver)
    while len(past_vers) < quan_vers:
        pher = 0
        ver = 0
        for i in range(quan_vers):
            if past_vers.count(i) > 0:
                continue
            if pher_matrix[cur_ver][i] > pher:
                ver = i
                pher = pher_matrix[cur_ver][i]

        next_ver = ver

        way_len += len_matrix[cur_ver][next_ver]
        cur_ver = next_ver
        past_vers.append(cur_ver)

    past_vers.append(start_ver)
    way_len += len_matrix[cur_ver][start_ver]

    return [way_len, past_vers]


def ants_alg():
    for i in range(ants_quan):
        way_len, past_vers = ant_cycle()

        delta_pher = cQ / len_regular(way_len)

        # испарение феромонов
        for j in range(len(len_matrix)):
            pher_matrix[j] = [(1 - pher_speed) * pher for pher in pher_matrix[j]]

        # распыление новых феромонов
        for j in range(len(past_vers) - 1):
            pher_matrix[past_vers[j]][past_vers[j + 1]] += delta_pher
    return greedy_ant()[0]


# Матрица длин
i = 0
cnt = 1
len_matrix = []
while i < cnt:
    a = list(map(int, input().split()))
    cnt = len(a)
    len_matrix.append(a)
    i += 1

quan_vers = len(len_matrix)
# Матрица начальных феромонов
pher_matrix = np.random.randint(1, 4, size=(quan_vers, quan_vers)).astype(float)

print(ants_alg())
