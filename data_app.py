import streamlit as st
from population import load_population, add_prefectures

st.set_page_config(layout='wide')

@st.cache_data
def get_tables():
    pop = load_population()
    pop_prefs = add_prefectures(pop)
    return (pop, pop_prefs)


pop, pop_prefs = get_tables()
pref_names = list(pop.index)
years = list(pop.columns)


POPULATION = 'https://www.e-stat.go.jp/stat-search/files?toukei=00200524&tstat=000000090001&tclass1=000000090004&tclass2=000001051180'
GEOLOCATIONS = 'https://gist.github.com/ctsaran/42728dad3c7d8bd91f1d'

cols3 = st.columns(3)
cols3[0].markdown('**推計人口 (2000~2015年)**')
cols3[1].link_button(':material/link:人口データ',POPULATION,help=f'総務省: {POPULATION}')
cols3[2].link_button('material/link:緯度経度データ',GEOLOCATIONS,help=f'Gist: {GEOLOCATIONS}')


table,graph,geolocation = st.tabs(['表','グラフ','地図'])

with table:
    st.dataframe(pop_prefs)


with graph:
    GRAPHS = {
        '折れ線グラフ': {
            'function': st.line_chart,
            'kwargs': {
                'x_labal': '年',
                'y_label': '人口 (単位千) '
            }
        },
        '棒グラフ': {
            'function': st.bar_chart,
            'kwargs': {
                'x_labal': '年',
                'y_label': '人口 (単位千) ',
                'stack': False
            }
        }
    }

    prefs = st.multiselect(
        label='表示する都道府県を選択してください',
        options=pref_names,
        help='未選択時はすべての都道府県が表示されます')
    cols2 = st.columns(2)
    trancepose = cols2[0].checkbox(
        label='転置',
        value=True
    )
    graph_type = cols2[1].radio(
        label='グラフタイプ',
        options=list(GRAPHS.keys()),
        horizontal=True
    )

    if len(prefs) > 0:
        pop =pop.loc[prefs]

    if trancepose is True:
        pop = pop.transpose()

    g =GRAPHS[graph_type]
    g['function'](data=pop, **g['kwargs'])


with geolocation:
    year = st.select_slider('年',years)
    st.map(
        data=pop_prefs,
        latitude='緯度',
        longitude='経度',
        size=year,
        color='#32CD33280'
    )