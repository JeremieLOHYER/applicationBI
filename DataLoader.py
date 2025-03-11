from datetime import datetime
from random import randint

import pandas as pd



class DataLoader:
    src_path = "data/"
    feature_names = ['CDSEXE', 'MTREV', 'NBENF', 'CDSITFAM', 'CDTMT', 'CDDEM', 'CDMOTDEM', 'CDCATCL']

    def error(self, data, text):
        return 'ID : ' + str(data['ID']) + ' ' + text

    def check_feature(self, data, feature_type):

        if feature_type == 'CDSEXE':
            sexe = data[feature_type]
            if sexe == 2 or sexe == 3 or sexe == 4:
                return None
            return self.error(data, 'sexe inconnu : ' + str(sexe))


        elif feature_type == 'MTREV':
            mtrev = data[feature_type]
            if mtrev >= 0 and mtrev < 50000:
                return None
            if mtrev > 0 and mtrev < 2000000: # 4 clients gros revenu et 1 > 1 000 000
                return None
            return self.error(data, 'revenu inconnu : ' + str(mtrev))


        elif feature_type == 'NBENF':
            nbenf = data[feature_type]
            if nbenf >= 0 and nbenf < 6:
                return None
            if nbenf >= 0  and nbenf < 7: # 1 avec 6 enfants
                return None
            return self.error(data, "beaucoup d'enfants : " + str(nbenf))


        elif feature_type == 'CDSITFAM':
            cdsitfam = data[feature_type]
            if cdsitfam == 'A' or cdsitfam == 'B' or cdsitfam == 'M' or cdsitfam == 'V' or \
                    cdsitfam == 'D' or cdsitfam == 'C' or cdsitfam == 'U' or cdsitfam == 'P' or \
                    cdsitfam == 'G' or cdsitfam == 'E' or cdsitfam == 'S' or cdsitfam == 'F':
                return None
            return self.error(data, 'sitfam inconnu : ' + cdsitfam)


        elif feature_type == 'CDTMT':
            cdtmt = data[feature_type]
            if cdtmt == 0 or cdtmt == 2:
                return None
            if cdtmt == 6: # 1 code societaire 6
                return None
            return self.error(data, 'statut societaire inconnu : ' + str(cdtmt))


        elif feature_type == 'CDDEM':
            cddem = data[feature_type]
            if cddem == 2:
                return None
            if cddem == 1:# 4 code demission 1
                return None
            return self.error(data, 'code demission inconnu : ' + str(cddem))


        elif feature_type == 'CDMOTDEM':
            cdmotdem = data[feature_type]
            if cdmotdem == 'DV' or cdmotdem == 'RA' or cdmotdem == 'DA':
                return None
            return self.error(data, 'motif demission inconnu : ' + cdmotdem)


        elif feature_type == 'CDCATCL':
            cdcatcl = data[feature_type]
            if cdcatcl == 21 or cdcatcl == 10 or cdcatcl == 25 or cdcatcl == 23 or cdcatcl == 24 or cdcatcl == 40:
                return None
            if cdcatcl == 22 or cdcatcl == 32: # 3 code 22 et 2 code 32
                return None
            return self.error(data, 'code categorie client inconnue : ' + str(cdcatcl))

        return None

    def getrange(self, s_range: str):
        if type(s_range) != str:
            return 0, range(0,1)
        t_range = s_range.split('  ')
        index = int(t_range[0], 16)
        rg = t_range[1].split('-')
        if rg[1] == '+':
            return index, range(int(rg[0]), int(rg[0]) + 1000)
        return index, range(int(rg[0]),int(rg[1]) + 1)

    def date(self, sdt: str):
        return datetime.strptime(sdt, "%d/%m/%Y").date()

    def getannee(self, s_range: str):
        t_range = s_range.split('  ')
        return int(t_range[0]), int(t_range[1])

    def check_DATES(self, data, sdtadh, sdtdem, sanneedem, agead, rangagead, agedem, rangagedem, rangdem, adh, rangadh):
        # ----- etape 1 ----- vérification de l'age du client :

        # age lors de l'adhesion
        indice_range_age_adhesion, range_age_adhesion = self.getrange(rangagead)
        if indice_range_age_adhesion < 1 or indice_range_age_adhesion > 8 :
            return self.error(data, 'identifiant tranche age client adhesion inconnue : ' + str(rangagead))
        if not agead in range_age_adhesion:
            return self.error(data, 'indice tranche age client adhesion incorrect : ' + str(agead) + ' VS ' + str(rangagead))

        # age lors de la demission
        indice_range_age_demission, range_age_demission = self.getrange(rangagedem)
        if indice_range_age_demission < 1 or indice_range_age_demission > 11:
            return self.error(data, 'identifiant tranche age client demission inconnue : ' + str(rangagedem))
        if not agedem in range_age_demission:
            return self.error(data, 'indice tranche age client demission incorrect : ' +str(agedem) + ' VS ' + str(rangagedem))

        if agedem < agead:
            return self.error(data, "age de démission inférieure a l'age d'adhesion : " + str(agedem) + ' VS ' + str(agead))

        # ----- etape 2 ----- vérification des dates d'adhesion/demission

        # conversion des données spéciales
        dtadh = self.date(sdtadh)
        dtdem = self.date(sdtdem)
        anneedem = int(sanneedem)

        # durée d'adhesion
        indice_range_duree_adhesion, range_duree_adhesion = self.getrange(rangadh)
        if indice_range_duree_adhesion < 0 or indice_range_duree_adhesion > 7:
            return self.error(data, 'indice duree adhesion inconnue : ' + str(rangadh))
        if not adh in range_duree_adhesion:
            return self.error(data, 'duree adhesion incorrecte : ' + str(adh) + ' VS ' + str(rangadh))

        if dtdem < dtadh:
            return self.error(data, "date de demission antérieure a la date d'adhesion " + str(dtdem) + ' VS ' + str(dtadh))

        # année de démission
        indice_annee_dem, annee_dem = self.getannee(rangdem)

        if indice_annee_dem < 0 or indice_annee_dem > 8:
            return self.error(data, 'indice annee demission inconnue : ' + str(rangdem))

        if anneedem != annee_dem:
            return self.error(data, 'annee de demission incorrecte : ' + str(anneedem) + ' VS ' + str(annee_dem))

        return None

    def checkData(self, data):

        e: str

        societaires = []

        for index, row in data.iterrows():
            for type in self.feature_names:
                e = self.check_feature(row, type)
                if e:
                    print(e)
            e = self.check_DATES(row, row['DTADH'],row['DTDEM'],row['ANNEEDEM'],row['AGEAD'],row['RANGAGEAD'],
                                 row['AGEDEM'],row['RANGAGEDEM'],row['RANGDEM'],row['ADH'],row['RANGADH'])
            if e:
                print(e)
            else:
                societaires.append(self.transform_demissionnaire_societaire(row))

        return societaires

    def estimation_date_naissance(self, data):
        sep_date_adhesion = str(data['DTADH']).split('/')
        age_adhesion = int(data['AGEAD'])


        annee_naissance = int(sep_date_adhesion[2]) - age_adhesion

        return '01/01/' + str(annee_naissance)

    def transform_demissionnaire_societaire(self, data):
        data_societaire = {'ID':0, 'CDSEXE': 0, 'DTNAIS': '0000-00-00', 'MTREV': 0, 'NBENF': 0, 'CDSITFAM': 0, 'DTADH': '31/12/1900', 'CDTMT': 0, 'CDMOTDEM': '', 'CDCATCL': 0, 'BPADH': '', 'DTDEM': '31/12/1900'}

        #Données communes
        data_societaire['ID'] = -data['ID']
        data_societaire['CDSEXE'] = data['CDSEXE']
        data_societaire['MTREV'] = data['MTREV']
        data_societaire['NBENF'] = data['NBENF']
        data_societaire['CDSITFAM'] = data['CDSITFAM']
        data_societaire['DTADH'] = data['DTADH']
        data_societaire['CDTMT'] = data['CDTMT']
        data_societaire['DTDEM'] = data['DTDEM']
        data_societaire['CDMOTDEM'] = data['CDMOTDEM']
        data_societaire['CDCATCL'] = data['CDCATCL']

        #DTNAIS estimée
        data_societaire['DTNAIS'] = self.estimation_date_naissance(data)

        return data_societaire


    def open_file(self, filename: str):
        # read input text and put data inside a data frame
        data = pd.read_csv(self.src_path + filename, delimiter=',')
        print(data.head())

        # print nb of instances and features
        print(data.shape)

        # print feature types
        print(data.dtypes)
        return data

    def get_data_as_societaire(self, filename: str):
        return pd.DataFrame(self.checkData(self.open_file(filename)))


if __name__ == '__main__':
    loader = DataLoader()

    data = loader.open_file('table1.csv')
    societaires = loader.checkData(data)

    print(societaires)