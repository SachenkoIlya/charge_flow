
import pandas as pd

class Parser:
    

    @staticmethod
    def to_df(data:list[dict]):
        return pd.DataFrame(data)