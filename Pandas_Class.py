import pandas as pd


class PandasDealer:
    def __init__(self):
        self.df = pd.read_csv("./gmails/contacts.csv")

    def read_emails(self):
        mails = self.df['emails'].values.tolist()
        return mails

