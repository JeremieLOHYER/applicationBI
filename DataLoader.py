

import pandas as pd



class DataLoader:
    src_path = "data/"
    feature_names = ['CDSEXE', 'MTREV', 'NBENF', 'CDSITFAM', 'CDTMT', 'CDDEM', 'CDMOTDEM', 'CDCATCL']

    def check_feature(self, data, feature_type):

        if feature_type == 'CDSEXE':
            sexe = data[feature_type]
            if sexe == 2 or sexe == 3 or sexe == 4:
                return None
            return 'ID : ' + str(data['ID']) + ' sexe inconnu : ' + str(sexe)


        elif feature_type == 'MTREV':
            mtrev = data[feature_type]
            if mtrev >= 0 and mtrev < 50000:
                return None
            # elif mtrev > 0 and mtrev < 2000000: # 4 clients gros revenu et 1 > 1 000 000
            #     return None
            return 'ID : ' + str(data['ID']) + ' revenu inconnu : ' + str(mtrev)


        elif feature_type == 'NBENF':
            nbenf = data[feature_type]
            if nbenf >= 0 and nbenf < 6:
                return None
            # if nbenf >= 0  and nbenf < 7: # 1 avec 6 enfants
            #     return None
            return "ID : " + str(data['ID']) + " beaucoup d'enfants : " + str(nbenf)


        elif feature_type == 'CDSITFAM':
            cdsitfam = data[feature_type]
            if cdsitfam == 'A' or cdsitfam == 'B' or cdsitfam == 'M' or cdsitfam == 'V' or \
                    cdsitfam == 'D' or cdsitfam == 'C' or cdsitfam == 'U' or cdsitfam == 'P' or \
                    cdsitfam == 'G' or cdsitfam == 'E' or cdsitfam == 'S' or cdsitfam == 'F':
                return None
            return 'ID : ' + str(data['ID']) + ' sitfam inconnu : ' + cdsitfam


        elif feature_type == 'CDTMT':
            cdtmt = data[feature_type]
            if cdtmt == 0 or cdtmt == 2:
                return None
            # if cdtmt == 6: # 1 code societaire 6
            #     return None
            return 'ID : ' + str(data['ID']) + ' statut societaire inconnu : ' + str(cdtmt)


        elif feature_type == 'CDDEM':
            cddem = data[feature_type]
            if cddem == 2:
                return None
            # if cddem == 1:# 4 code demission 1
            #     return None
            return 'ID : ' + str(data['ID']) + ' code demission inconnu : ' + str(cddem)


        elif feature_type == 'CDMOTDEM':
            cdmotdem = data[feature_type]
            if cdmotdem == 'DV' or cdmotdem == 'RA' or cdmotdem == 'DA':
                return None
            return 'ID : ' + str(data['ID']) + ' motif demission inconnu : ' + cdmotdem


        elif feature_type == 'CDCATCL':
            cdcatcl = data[feature_type]
            if cdcatcl == 21 or cdcatcl == 10 or cdcatcl == 25 or cdcatcl == 23 or cdcatcl == 24 or cdcatcl == 40:
                return None
            # if cdcatcl == 22 or cdcatcl == 32: # 3 code 22 et 2 code 32
            #     return None
            return 'ID : ' + str(data['ID']) + ' code categorie client inconnue : ' + str(cdcatcl)

        return None

    def check_DATES(self, dtadh, datedem, anneedem, agead, rangagead, agedem, rangagedem, rangdem, adh, rangadh):
        return None
        return "date adhesion incorrecte : " + dtadh
        return "date demission incorrecte : " + datedem
        return "annee demission incorrecte : " + anneedem
        return 'age adhesion incorrect : ' + agead

    def checkData(self, data):

        e: str

        for index, row in data.iterrows():
            for type in self.feature_names:
                e = self.check_feature(row, type)
                if e:
                    print(e)
            e = self.check_DATES(row['DTADH'],row['DTDEM'],row['ANNEEDEM'],row['AGEAD'],row['RANGAGEAD'],
                                 row['AGEDEM'],row['RANGAGEDEM'],row['RANGDEM'],row['ADH'],row['RANGADH'])
            if e:
                print(e)


        return None


    def open_file(self, filename: str):
        # read input text and put data inside a data frame
        data = pd.read_csv(self.src_path + filename, delimiter=',')
        print(data.head())

        # print nb of instances and features
        print(data.shape)

        # print feature types
        print(data.dtypes)
        return data


if __name__ == '__main__':
    loader = DataLoader()

    data = loader.open_file('table1.csv')
    loader.checkData(data)