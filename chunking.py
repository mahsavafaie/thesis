import glob
import os
import pandas as pd

noise_labels={'sil', 'ns', 'br', 'noise', 'nnss','laugh','start','cw', ''}

output = 'D:/asset/data/tfarsdat/Word/sentences'

def detect_sent(df):
    """Make a column with integer denoting sentence number of each row"""
    i = 0
    out = []
    for row in df['Phonemic'].values:
        out.append(i)
        if row in noise_labels:
            i += 1
    return out

def task(sent):
    """For a given sentence, format as string and get boundaries"""
    # inverse boolean indexing based on a column's values
    # make a list of true/false, the same length as the sent
    filt = sent['Phonemic'].isin(noise_labels)
    # cut down sent to just good tokens
    sent = sent[~filt]
    if not len(sent):
        return pd.Series([None, None, None])
    text = sent['Phonetic'].str.cat(sep=' ')
    return pd.Series([text, sent.iloc[0]['Start'], sent.iloc[-1]['End']])

# iterate over each file, read in, process and save
for filename in glob.glob('D:/asset/data/tfarsdat/Word/csv/*.csv'):
    print(filename)
    df = pd.read_csv(filename, header=0, encoding="iso8859_15").fillna('')
    df['Sentence'] = detect_sent(df)
    # run main processing, remove empty sentences, round floats and drop old index
    starts = df.groupby('Sentence').apply(task).dropna().round(3).reset_index(drop=True)
    # increment index so first sentence is 1
    starts.index += 1
    # give useful column names
    starts.columns = ["Text", "Start", "End"]
    # make sure we have output directory
    if not os.path.isdir(output):
        os.makedirs(output)
    # save csv with tab sep
    outpath = os.path.join(output, os.path.basename(filename))
    starts.to_csv(outpath, sep='\t')
