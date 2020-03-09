import os
import csv
import pandas as pd
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def merge_txt(path):
	file_names = []
	for files in os.listdir(path):
		if '.txt' in files:
			file_names.append(files)
	names = []
	def merge_names(path):
		for name in file_names:
			def find_all_names(name, path):
				file = open(path + name, 'r')
				for line in file:
					if 'Name:' in line:
						line = line.strip('\n')
						name = line.replace('Name: ', '')
						name = name.replace("'", '')
						names.append(name)
				return(names)
			all_names = []
			all_names = all_names + find_all_names(name, path)
		return(all_names)
	purposes = []
	def merge_purposes(path):
		for name in file_names:
			def  find_all_purposes(name, path):
				file = open(path + name, 'r')
				for line in file:
					if 'Purpose:' in line:
						line = line.strip('\n')
						line = line.strip('(')
						line = line.replace(')', '')
						purpose = line.replace('Purpose: ', '')
						purpose = purpose.replace("'", '')
						purposes.append(purpose)
				return(purposes)
			all_purposes = []
			all_purposes = all_purposes + find_all_purposes(name, path)
		return(all_purposes)
	Name = merge_names(path)
	Purpose = merge_purposes(path)
	merge_txt = pd.DataFrame({'Name':Name, 'Purpose':Purpose})
	return(merge_txt)

def merge_table(filename):
    file_name = []
    for files in os.listdir(filename):
        if '.txt' in files:
            file_name.append(files)
    for name in file_name:
        dataframe = pd.DataFrame()
        def txt_table(filename, name):
            f = open(filename + name, 'r')
            rows = f.readlines()
            table_col1 = rows[1].split('|')[1].strip()
            table_col2 = rows[1].split('|')[2].strip()
            name = []
            purpose = []
            for i in range(3, len(rows)-1):
                row = rows[i].split('|')
                left = row[1]
                right = row[2]
                left = left.strip(' ')
                right = right.strip(' ')
                name.append(left)
                purpose.append(right)
                dataframe = pd.DataFrame()
                dataframe[table_col1] = name
                dataframe[table_col2] = purpose
            return(dataframe)
        df = txt_table(filename, name)
    result = df.append(df)
    return(result)

def merge_all(path):
    merge_all = pd.DataFrame()
    file_list = []
    for file in os.listdir(path):
        if '.csv' in file:
            file_list.append(file)    
    def merge_names(path):
        names = []
        for file in file_list:
            def all_name(path,file):
                f = open(path + file, 'r')
                reader = csv.DictReader(f)
                name = [row['Name'] for row in reader]
                return(name)
            names = names + all_name(path,file) 
        return(names)
   
    def merge_purposes(path):
        purposes = []
        for file in file_list:
            def all_purposes(path, file):
                f = open(path + file,'r')
                reader = csv.DictReader(f)
                purpose = [row['Purpose'] for row in reader]
                return(purpose)
            purposes = purposes + all_purposes(path, file)
        return(purposes)
    Name = merge_names(path)
    Purpose = merge_purposes(path)
    merge_all = pd.DataFrame({'Name':Name, 'Purpose':Purpose})
    return(merge_all) 

def purposes_scores(file):
    f = open(file, 'r')
    reader = csv.DictReader(f)
    purpose = [row['Purpose'] for row in reader]
    scores = []
    for text in purpose:
        analyser = SentimentIntensityAnalyzer()
        def sentiment_analysis(text):
            score = analyser.polarity_scores(text)
            return(score)
        scores.append(sentiment_analysis(text))
        compounds = []
        for dict in scores:
            compound = dict['compound']
            compounds.append(compound)
    data = pd.read_csv(file)
    data['Compound'] = compounds
    return(data)

def worse_best(file):
    data = purposes_scores(file)
    list = [(data['Name'][i], data['Compound'][i]) for i in range(0, len(data))]
    list.sort(key = lambda x:x[1])
    worse = list[0:5]
    best = list[-6:-1]
    result = {
        'Best':best,
        'Worse':worse
    }
    return(result)

if __name__ == "__main__":
    path = '/Users/yuechenjiang/Desktop/FE595/FE595HW3/Companys/' 
    filename = '/Users/yuechenjiang/Desktop/FE595/FE595HW3/Companys/txt_table/'
    merge_txt(path).to_csv('merge_txt.csv',index = False)
    merge_table(filename).to_csv('merge_table.csv', index = False)
    merge_all(path).to_csv('merge_all.csv', index = False)
    file = path + 'merge_all.csv'
    purposes_scores(file).to_csv(path + 'Scores.csv', mode = 'a',index =False)
    worse_best(file)

'''
Best
 [('Day, Williams and Diaz', 0.743), 
 ('Hall, Heath and Perez', 0.743), 
 ('Cabrera, Levine and Underwood', 0.7579), 
 ('Barajas LLC', 0.765), 
 ('Roberts-Huff', 0.7717), 
 ('Stokes and Sons', 0.7845)]
 Worse
 [('Mcclain, Mccarthy and Lozano', -0.6486), 
 ('Huffman, Norton and Cantu', -0.6486), 
 ('Washington-Mccormick', -0.6486), 
 ('Medina-Dorsey', -0.6486), 
 ('Willis and Sons', -0.6486)]
 '''