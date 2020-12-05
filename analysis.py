## ANALYSIS

def analyze(filename):

    data = pd.read_csv(filename)

    def get_responses(data):
        return data[['img', 'earlyResp', 'resp', 'lateResp']]

    def fill_row(row):
        if np.isnan(row['resp']):
            if not np.isnan(row['lateResp']):
                return row['lateResp']
            elif not np.isnan(row['earlyResp']):
                return row['earlyResp']
            else:
                return -1
        return row['resp']

    def clear_blanks(tbl):
        tbl['resp'] = tbl.apply(fill_row, axis=1)
        return tbl[tbl['resp'] != -1][['img', 'resp']]

    valid_resp = clear_blanks(get_responses(data))

    def score_hits_misses(row):
        if 'a' in row['img']:
            if row['resp'] == 4 or row['resp'] == 3:
                return 1
            elif row['resp'] == 1 or row['resp'] == 2:
                return 0
        elif 'b' in row['img'] or 'foil' in row['img']:
            if row['resp'] == 4 or row['resp'] == 3:
                return 0
            elif row['resp'] == 1 or row['resp'] == 2:
                return 1

    valid_resp['correctness'] = valid_resp.apply(score_hits_misses, axis=1)

    lures = valid_resp[valid_resp['img'].str.contains('b')]
    novels = valid_resp[valid_resp['img'].str.contains('foil')]

    def score_FA_CR(tbl):
        return 1 - tbl['correctness']

    lures['FA'] = score_FA_CR(lures)
    novels['FA'] = score_FA_CR(novels)

    def gather_results(lures, novels):
        """Returns a dictionary of String: Double describing accuracy"""
        lures_FA = np.mean(lures['FA'])
        lures_CR = 1 - lures_FA
        novels_FA = np.mean(novels['FA'])
        novels_CR = 1 - novels_FA
        return {'Lure FA': lures_FA,
               'Lure CR': lures_CR, 
               'Novel FA': novels_FA, 
               'Novel CR': novels_CR}

    res = gather_results(lures, novels)

    def LDI(lureCR, novelFA):
        return lureCR - novelFA

    outputName = filename[:-8] + "RESULTS.csv"
    ouputFile = open(outputName, 'w')
    writer = csv.writer(ouputFile, delimiter=',')
    for k, v in res.items():
        writer.writerow([k, v])
    ouputFile.close()