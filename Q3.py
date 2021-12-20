import cvxpy


def Nash_budget(total: float, subject: list, preferences: list):
    size_of_subject = len(subject)
    size_of_citizens = len(preferences)
    allocations = cvxpy.Variable(size_of_subject)

    utilities = [0] * size_of_citizens
    donations = [total / size_of_citizens] * size_of_citizens

    # temp_dic = {0:'a', 1:'b', 2:'c' ......}
    temp_dic = {i: subject[i] for i in range(size_of_subject)}

    for citizen in range(size_of_citizens):
        for sub in range(len(preferences[citizen])):
            rep_sub = get_key(temp_dic, preferences[citizen][sub])
            preferences[citizen][sub] = rep_sub

    for citizen in range(size_of_citizens):
        for sub in preferences[citizen]:
            utilities[citizen] = utilities[citizen] + allocations[sub]

    sum_of_logs = cvxpy.sum([cvxpy.log(u) for u in utilities])
    positivity_constraints = [v >= 0 for v in allocations]
    sum_constraint = [cvxpy.sum(allocations) == sum(donations)]

    problem = cvxpy.Problem(
        cvxpy.Maximize(sum_of_logs),
        constraints=positivity_constraints + sum_constraint)
    problem.solve()

    for citizen in range(size_of_citizens):
        print(f"Citizen {citizen} gives", end=" ")
        counter = len(preferences[citizen])
        for sub in preferences[citizen]:
            print((allocations[sub].value * donations[citizen] / utilities[citizen].value), end=" ")
            print(f"to {temp_dic[list(temp_dic.keys()).index(sub)]}", end=" ")
            if counter > 1:
                print("and", end=" ")
                counter = counter - 1
        print()


def get_key(dic, val):
    for k, v in dic.items():
        if val == v:
            return k


if __name__ == '__main__':
    # Example from the class:

    total = 500
    subject = ['a', 'b', 'c', 'd']
    subject_of_each_citizen = [['a', 'b'], ['a', 'c'], ['a', 'd'], ['b', 'c'], ['a']]
    Nash_budget(total, subject, subject_of_each_citizen)

    # should print:
    # Citizen 0 gives 85 to a and 15 to b
    # Citizen 1 gives 85 to a and 15 to c
    # Citizen 2 gives 100 to a and 0 to d
    # Citizen 3 gives 50 to b and 50 to c
    # Citizen 4 gives 100 to a
