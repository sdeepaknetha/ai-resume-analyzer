import matplotlib.pyplot as plt


def create_skill_chart(matched, missing):

    labels = ["Matched Skills", "Missing Skills"]

    values = [len(matched), len(missing)]

    plt.figure()

    plt.bar(labels, values)

    plt.title("Skill Match Chart")

    plt.ylabel("Number of Skills")

    chart_path = "skill_chart.png"

    plt.savefig(chart_path)

    plt.close()

    return chart_path
