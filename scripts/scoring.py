import pandas as pd
from tabulate import tabulate

filepath = '../resources/top_scorers.csv'


def top_scorers():
    df = pd.read_csv(filepath)
    pprint_df(df.head(10))


def pprint_df(dframe):
    print(tabulate(dframe, headers='keys', tablefmt='psql', showindex=False))


class ScoreBoard:

    def __init__(self, score, username, character_name):
        self.score = score
        self.username = username
        self.char_name = character_name
        self.update_scoreboard()

    def update_scoreboard(self):
        df = pd.read_csv(filepath)
        # df.sort_values(by=['Points'], ascending=False, ignore_index=True, inplace=True)
        rec = df.to_records()
        for char_dict in rec:
            if char_dict[2] == self.username:
                idx = char_dict[0]
                df = df.drop(labels=idx, axis=0)

        new_data = pd.Series({'Position': 1, 'Username': self.username, 'Character Name': self.char_name,
                              'Points': self.score})
        new_df = pd.concat([df, new_data.to_frame().T], ignore_index=True)
        new_df.sort_values(by=['Points'], ascending=False, ignore_index=True, inplace=True)
        data = new_df.to_dict()
        cnt = 0
        for n in (data['Position']):
            cnt += 1
            # print(data['Position'][n])
            data['Position'][n] = cnt

        data = df.from_dict(data)

        data.to_csv(filepath, index=False)
