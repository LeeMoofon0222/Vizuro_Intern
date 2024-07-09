import pandas as pd

def remove_zero_rows_and_columns(input_file, output_file):

    df = pd.read_csv(input_file)
    
    

    df_numeric = df.iloc[1:, 1:].apply(pd.to_numeric, errors='coerce')

    non_zero_rows = (df_numeric.fillna(0) != 0).any(axis=1)
    df_filtered = pd.concat([df.iloc[:1], df.iloc[1:][non_zero_rows]])

    non_zero_columns = (df_numeric.fillna(0) != 0).any(axis=0)
    df_filtered = pd.concat([df_filtered.iloc[:, :1], df_filtered.iloc[:, 1:].loc[:, non_zero_columns]], axis=1)
    
    df_filtered.to_csv(output_file, index=False)

if __name__ == '__main__':
    input_file = 'dag.csv'
    output_file = 'importance.csv'
    remove_zero_rows_and_columns(input_file, output_file)