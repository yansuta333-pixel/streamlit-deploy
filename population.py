from pathlib import PurePath
import pandas as pd

PARENT = PurePath(__file__).parent

URL = 'https://www.e-stat.go.jp/stat-search/file-download?statInfId=000013168605&fileKind=4'
PREFECTURES = PARENT / 'data/prefectures.csv'

def load_population():
    df = pd.read_excel(
        io=URL,
        sheet_name=0,
        usecols='C,E:T',
        index_col=0,
        skiprows=list(range(8))+[9, 10]+list(range(58, 65))
    )

    df.rename(index=lambda x: x.replace(' ',''), inplace=True)
    df.rename(columns=lambda x: f'Y{x}', inplace=True)
    df.columns.name = '都道府県名'

    return df


def add_prefectures(pop):
    prefs = pd.read_csv(
        PREFECTURES,
        index_col=0
    )
    df = prefs.merge(pop, left_index=True, right_index=True)

    return df


if __name__ == '__main__':
    pop = load_population()
    prefs = add_prefectures(pop)

    print('都道府県:', list(pop.index))
    print(prefs)
    print(prefs.loc[['東京都','神奈川県']])
    print(prefs.transpose())
