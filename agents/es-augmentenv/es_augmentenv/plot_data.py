import json
import os.path
import re
import matplotlib.pyplot as plt
from ordered_set import OrderedSet

colors = {
    0: 'r',
    1: 'g',
    2: 'b',
    3: 'c',
    4: 'm',
    5: 'y',
    6: 'k'
}


def plot_data(datasets, x_s, y_s, names, title='title'):
    plt.set_cmap("viridis")
    if len(datasets) != len(names):
        raise Exception("length of datasets and names must match")
    for j in range(len(datasets)):
        data = datasets[j]
        name = names[j]
        if len(x_s) != len(y_s):
            raise Exception("length of x_s and y_s must match")
        for i in range(len(x_s)):
            plt.plot([datum[x_s[i]] for datum in data], [datum[y_s[i]] for datum in data], label=name)
            plt.xlabel(x_s[i])
            plt.ylabel(y_s[i])
    plt.title(title)
    plt.legend()
    plt.savefig(f"plots/{title}")
    plt.show()


def remove_dt(name):
    return re.split(r"_(\d{2})_(\d{2})_(\d{2})_(\d{2})_(\d{2})_(\d{2})", name)[0]


def plot_data_clean(datasets, x_s, y_s, names, title='title'):
    if len(datasets) != len(names):
        raise Exception("length of datasets and names must match")

    # sort data by name
    names = [remove_dt(name) for name in names]
    name_set = OrderedSet(names)
    name_idxs = [[] for _ in range(len(name_set))]
    # iterate through each name
    for idx, name in enumerate(names):
        # check which set it belongs to
        for set_num, set_name in enumerate(name_set):
            if name == set_name:
                name_idxs[set_num].append(idx)
                break

    # iterate over name_set, plot accouring to color
    for i, idx_set in enumerate(name_idxs):
        name = name_set[i]
        for k, idx in enumerate(idx_set):
            data = datasets[idx]
            for j in range(len(x_s)):
                plt.plot([datum[x_s[j]] for datum in data], [datum[y_s[j]] for datum in data], label="_nolengend_" if k > 0 else name, color=colors[i])
                plt.xlabel(x_s[j])
                plt.ylabel(y_s[j])
    plt.title(title)
    plt.legend()
    plt.savefig(f"plots/{title}")
    plt.show()


def main(title, gen=True, comparisons=True, plot_together=True, subdir='', clean=True):
    file_dir = os.path.join(os.path.dirname(__file__), f"saved_train_data/{subdir}")

    if plot_together:
        paths = [file_path for file_path in os.listdir(file_dir) if not file_path.startswith('.')]
        datasets = [json.load(open(os.path.join(file_dir, path))) for path in paths]
        names = [os.path.splitext(path)[0] for path in paths]

        plot_func = plot_data_clean if clean else plot_data
        if gen:
            plot_func(datasets, ["gen"], ["best_true_reward"], names, title)
        if comparisons:
            plot_func(datasets, ["comparisons"], ["best_true_reward"], names, title)

    else:
        for file_path in os.listdir(file_dir):
            if file_path.startswith('.'):
                continue
            path = os.path.join(file_dir, file_path)

            # load training data
            f = open(path)
            train_data = json.load(f)

            name = os.path.splitext(file_path)[0]
            if gen:
                plot_data([train_data], ["gen"], ["best_true_reward"], [name])
                # plot_data([train_data], ["gen"], ["best_reward"], name)
            if comparisons:
                plot_data([train_data], ["comparisons"], ["best_true_reward"], [name])
                # plot_data([train_data], ["comparisons"], ["best_reward"], [name])


if __name__ == "__main__":
    main(title="optimizer", subdir="optim", comparisons=False, clean=True)
    main(title="morphology", subdir="morph", comparisons=False, clean=True)
    main(title="population size", subdir="popsize", comparisons=False, clean=True)
    main(title="predictor", subdir="predictor", comparisons=False, clean=True)
    main(title="variation", subdir="sigma", comparisons=False, clean=True)
    main(title="rm training iters", subdir="train_iters", comparisons=False, clean=True)


