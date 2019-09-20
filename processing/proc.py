import pickle,pandas as pd,numpy as np

class data_cleaning():
    def __init__(self,dataframe):
        self.dataframe = dataframe
        self.subjects = self.dataframe[self.dataframe.columns[3:14]]

    converted = None



    def convert(self,x):
        return int(x)

    def conversion(self):
        for subj in self.subjects:
            self.subjects[subj] = self.subjects[subj].agg(self.convert)
        converted = pd.concat((self.dataframe[self.dataframe.columns[:3]], self.subjects),axis=1)
        converted['Total'] = self.subjects.sum(axis=1)
        converted.index = converted["Adm No"]

        return converted

class grading():
    def __init__(self, dataframe):
        self.dataframe = dataframe

    science_subjects = ['Mathematics', 'Physics', 'Biology', 'Chemistry']


    def total_grade(self,value):
        value = round(value)
        if value in range(700,1100):
            return "A"
        elif value in range(550,700):
            return "B"
        elif value in range(400,550):
            return "C"
        elif value in range(300,400):
            return "D"
        else:
            return "E"

    def science_subject_grade(self,value):
        value = round(value)
        if value in range(70, 100):
            return "A"
        elif value in range(65, 70):
            return "B"
        elif value in range(55, 65):
            return "C"
        elif value in range(40, 55):
            return "D"
        else:
            return "E"

    def other_subject_grade(self,value):
        value = round(value)
        if value in range(80, 100):
            return "A"
        elif value in range(70, 80):
            return "B"
        elif value in range(60, 70):
            return "C"
        elif value in range(50, 60):
            return "D"
        else:
            return "E"

    def grading(self):
        self.dataframe['Grade']  = self.dataframe['Total'].agg(self.total_grade)
        return self.dataframe

    def number_of_overall_grades(self):

        return self.dataframe['Grade'].value_counts()

    def science_grades(self):
        average = (self.dataframe["Mathematics"] + self.dataframe["Physics"] + self.dataframe["Chemistry"] + self.dataframe["Biology"]) / 4
        grade = pd.Series([round(self.dataframe.loc[i]["Total"] / 11) for i in self.dataframe.index.tolist()],index=self.dataframe.index)
        return pd.concat([average,average.agg(self.science_subject_grade),grade],axis=1)

    def arts_grades(self):
        average = (self.dataframe["English"] + self.dataframe["Kiswahili"] + self.dataframe["Geography"] + self.dataframe["History"]) / 4
        grade = pd.Series([round(self.dataframe.loc[i]["Total"] / 11) for i in self.dataframe.index.tolist()],index=self.dataframe.index)
        return pd.concat([average,average.agg(self.other_subject_grade),grade],axis=1)

    def math_grades(self):
        average = pd.Series(self.dataframe["Mathematics"].values.tolist(),index = self.dataframe.index.tolist())
        grade = pd.Series([round(self.dataframe.loc[i]["Total"] / 11) for i in self.dataframe.index.tolist()],index=self.dataframe.index)

        return pd.concat([average,average.agg(self.science_subject_grade),grade],axis=1)

    def grades_per_subject(self,subject):
        res = self.dataframe[subject]
        if subject in self.science_subjects:
            return pd.Series(res.agg(self.science_subject_grade).values.tolist(), index=self.dataframe["Student Name"].values.tolist())
        else:
            return pd.Series(res.agg(self.other_subject_grade).values.tolist(), index=self.dataframe["Student Name"].values.tolist())

    def number_of_subject_grades(self,subject):

        return self.grades_per_subject(subject).value_counts()

class rankings():
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.subjects = self.dataframe[self.dataframe.columns[3:14]]

    def number_rankings(self):
        self.dataframe['Number'] = self.dataframe['Total'].rank(ascending=False)
        self.dataframe = self.dataframe.sort_values(by="Number")
        return  self.dataframe



    def subject_rankings(self):
        return self.subjects.mean().rank().sort_values().rank(ascending=False)

    def number_rankings_per_subject(self):
        subj_rank = pd.concat([self.dataframe[['Adm No','Student Name']],self.subjects.rank(ascending = False)],axis=1)
        return subj_rank

class contribution():
    def __init__(self,dataframe):
        self.dataframe = dataframe
        self.subjects = self.dataframe.columns[3:15].values.tolist()

    def individual_subject_contribution(self,number): #accepts series as input
        result = []
        values = self.dataframe.iloc[number][self.subjects]
        for val in values:
            result.append(round((float(val / values.iloc[-1]) * 100),2)) #total should be the last value
        ser = pd.Series(result,index=[col for col in self.subjects])
        return ser

    def weak_contribution(self, grade):

        weak_grade = self.dataframe['Grade'] == grade
        for val in self.dataframe.where(weak_grade).dropna().iterrows():
            result = []
            for x in val[1][3:15]:
                result.append(round((float(x / val[1][3:15][-1]) * 100), 2))
            return pd.Series(result,index=[col for col in self.subjects])

class correlation():
    def __init__(self,dataframe):
        self.dataframe = dataframe
        self.subjects = self.dataframe[3:14]

    def corr(self):
        result = self.dataframe.corr()
        return result
