import matplotlib
from matplotlib import pyplot as plt
import numpy as np
matplotlib.use('Agg')

font = {'family': 'Cambria, Cochin, Georgia, Times, "Times New Roman", serif',
        'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)

def get_skills(a_dictionary):
    skill_names = []
    for skill in a_dictionary.keys():
        skill = skill.capitalize()
        skill_names.append(skill)
    return skill_names


def get_frequency_values(a_dictionary):
    frequencies = []
    for skill in a_dictionary:
        value = a_dictionary.get(skill)
        frequencies.append(value)
    return frequencies


def create_bar_chart(filtered_skills):
    a_dict = dict(filtered_skills)
    skills = get_skills(a_dict)
    values = get_frequency_values(a_dict)

    x = np.arange(len(skills))
    width = 0.5

    fig, ax = plt.subplots(figsize=(35, 15))
    rect = ax.bar(x, values, width)

    ax.set_ylabel('Frequency')
    ax.set_xticks(x)
    ax.set_xticklabels(skills)

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rect)

    return fig
