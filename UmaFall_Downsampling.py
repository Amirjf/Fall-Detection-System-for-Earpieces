import os

import numpy as np
import csv
import glob
import pandas as pd
from scipy import signal
from scipy import interpolate



def Downsampled(diretorio_raiz, old_freq, new_freq):
        
        taxa_amostragem_original = old_freq  # Hz
        taxa_amostragem_desejada = new_freq  # Hz
        # Desired downsampling factor
        fator_downsampling = int(taxa_amostragem_original/taxa_amostragem_desejada)
        
            
        # Traverse all subfolders and CSV files
        for pasta_atual, subpastas, arquivos in os.walk(diretorio_raiz):
            for arquivo_entrada in arquivos:
                if arquivo_entrada.endswith('.csv'):
                    caminho_arquivo = os.path.join(pasta_atual, arquivo_entrada)
            
                    
                    # Read the CSV file into a DataFrame
                    df = pd.read_csv(caminho_arquivo)
        
                    # Extract the header from the original file
                    cabeçalho = list(df.columns)
        
                    # Select only the columns of interest for downsampling
                    colunas_interesse = cabeçalho[1:7]
        
                    # Perform downsampling on the data
                    dados_downsampled = df[colunas_interesse].iloc[::fator_downsampling]
                    tempo_downsampled = df['TimeStamp'].iloc[::fator_downsampling]
                    info_downsampled = df.iloc[::fator_downsampling, 7:]
        
                    # Create a new DataFrame with the downsampled data and original information
                    df_downsampled = pd.concat([tempo_downsampled, dados_downsampled, info_downsampled], axis=1)
        
                    # Create the destination path for the new CSV file
                    nome_arquivo = os.path.splitext(arquivo_entrada)[0]
                    caminho_arquivo_downsampled = os.path.join(pasta_atual, nome_arquivo + '.csv')
        
                    # Save the downsampled data to a new CSV file, keeping the original header
                    df_downsampled.to_csv(caminho_arquivo_downsampled, index=False, header=cabeçalho)
