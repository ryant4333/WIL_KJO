import sys
import matplotlib.pyplot as plt

sys.path.insert(1, "./src/")
import plot_graph

def wrapper(f, title=None):
    """Used for the user to graph objective logs.\n
    First variable is required and its the path to the objective log.\n
    Second variable is the title of the graph and is optional."""
    
    plot_graph.graph(f, title)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise AttributeError("Missing directory to objective log")
    f = sys.argv[1]

    if len(sys.argv) < 3:
        title = None
    else:
        title = sys.argv[2]

    wrapper(f, title)