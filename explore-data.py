import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from DataLoader import DataLoader


def print_sep():
    print('\n--------------------------------------------------------\n')


def hist_per_col(data, col, prefix):
    plt.figure(figsize=(10, 5))
    sns.histplot(data[col], bins=50, color='red', alpha=0.5)

    plt.title('Distribution des ' + col)
    plt.xlabel('Montant des ' + col)
    plt.ylabel('Nombre de clients')

    plt.savefig('fig/hist-col-' + prefix + col.lower())
    plt.close()


def cat_per_col(data, col):
    cat = pd.Categorical(data[col])

    print(f'Colonne {col}')
    print(cat.describe())

    categories = []
    for cat in cat.categories:
        categories.append(str(cat))

    print(f'Valeurs presentes: {', '.join(categories)}')


def pca(data, numerical_cols, name):
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(data[numerical_cols])

    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(df_scaled)

    df_pca = pd.DataFrame(pca_result, columns=['PC1', 'PC2'])

    print('Variance expliquée par chaque composante :', pca.explained_variance_ratio_)

    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=df_pca["PC1"], y=df_pca["PC2"], alpha=0.5)
    plt.xlabel('Première composante principale (PC1)')
    plt.ylabel('Deuxième composante principale (PC2)')
    plt.title('Projection des données sur les deux premières composantes')
    plt.savefig('fig/pca-' + name)
    plt.close()

    pca = PCA()
    pca.fit(df_scaled)

    plt.figure(figsize=(8, 5))
    plt.plot(range(1, len(numerical_cols) + 1), np.cumsum(pca.explained_variance_ratio_), marker='o', linestyle='--')
    plt.xlabel('Nombre de composantes')
    plt.ylabel('Variance expliquée cumulée')
    plt.title('Scree plot - Choix du nombre de composantes')
    plt.savefig('fig/pca-var-cum-' + name)
    plt.close()


if __name__ == '__main__':
    demissionaires = pd.read_csv('data/table1.csv')

    loader = DataLoader()
    societaires = pd.concat([pd.read_csv('data/table2.csv'), loader.get_data_as_societaire('table1.csv')], ignore_index=True)

    dem_columns = list(demissionaires.columns)
    soc_columns = list(societaires.columns)

    print(f'Nombre de demissionaires: {len(demissionaires)}')
    print(f'Nombre de societaires: {len(societaires)}')

    print_sep()

    print(f'Colonne de demissionaires: {dem_columns}')
    print(f'Colonne de societaires: {soc_columns}')
    print('Colonne en commun: ' + str([col for col in dem_columns if col in soc_columns]))

    print_sep()

    print(demissionaires.describe())
    print(societaires.describe())

    print_sep()

    no_rev_count = demissionaires.loc[demissionaires['MTREV'] > 0]
    print(f'Nombre de demissionaires avec un revenu: {len(no_rev_count)}')

    print_sep()

    cat_per_col(demissionaires, 'CDSEXE')
    print()
    cat_per_col(demissionaires, 'CDSITFAM')
    print()
    cat_per_col(demissionaires, 'CDMOTDEM')
    print()
    cat_per_col(demissionaires, 'CDCATCL')

    hist_per_col(demissionaires, 'MTREV', 'dem-')
    hist_per_col(demissionaires, 'NBENF', 'dem-')
    hist_per_col(demissionaires, 'ANNEEDEM', 'dem-')

    print_sep()

    print(f"Nombre de societaires demissionaires: {len(societaires.loc[societaires['DTDEM'] != '31/12/1900'])}")

    print_sep()

    societaire_cat_cols = ['CDSEXE', 'CDSITFAM', 'CDTMT', 'CDMOTDEM', 'CDCATCL']

    for societaire_cat_col in societaire_cat_cols:
        cat_per_col(societaires, societaire_cat_col)
        print_sep()

    hist_per_col(societaires, 'MTREV', 'soc-')
    hist_per_col(societaires, 'NBENF', 'soc-')

    numerical_dem_cols = ['MTREV', 'NBENF']
    pca(demissionaires, numerical_dem_cols, 'dem')
