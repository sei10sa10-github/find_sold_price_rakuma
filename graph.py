import pandas as pd
from pandas import DataFrame
import os
import matplotlib.pyplot as plt


def save_graph():
    df = read_csv()
    df = df[df['sold']]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    price = df['price']
    min_price = price.min()
    max_price = price.max()

    print(price.describe())
    
    ax.hist(price, bins=50, range=(3000, 10000))
    fig.show()
    plt.savefig('figure.png')


def read_csv() -> DataFrame:
    abs_file_path = os.path.join(os.getcwd(), 'data.csv')

    with open(abs_file_path, 'r') as f:
        df = pd.read_csv(f)
        return df


if __name__ == '__main__':
    save_graph()