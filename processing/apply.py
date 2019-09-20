from .proc import  *

class processing():
    def __init__(self,dataframe,teacher):
        self.dataframe = dataframe
        self.subjects = self.dataframe.columns[3:14]
        self.science_subjects = ["Maths","Physics","Biology","Chemistry"]
        self.teacher = teacher

    def clean(self):
        global results
        results = grading(rankings(data_cleaning(self.dataframe).conversion()).number_rankings()).grading()
        results = results.where(results["Adm No"]!=0).dropna()

    def number_of_grades(self):
        grade = ["A", "B", "C", "D", "E"]
        lis = {}
        for gr in grade:
            try:
                lis[gr] = grading(results).number_of_overall_grades()[gr]
            except KeyError:
                lis[gr] = 0
        return pd.Series([i for i in lis.values()], index=grade)

    def grades_per_subject(self,subject):
        return grading(results).grades_per_subject(subject)

    def science(self):
        return grading(results).science_grades()
    def math(self):
        return grading(results).math_grades()
    def arts(self):
        return grading(results).arts_grades()

    def number_of_subject_grades(self,subject):
        grade = ["A","B","C","D","E"]
        lis = {}
        for gr in grade:
            try:
                lis[gr] = grading(results).number_of_subject_grades(subject)[gr]
            except KeyError:
                lis[gr] = 0
        return pd.Series([i for i in lis.values()],index=grade)

    def subject_rankings(self):
        return rankings(results).subject_rankings()

    def number_rankings_per_subject(self):
        return rankings(results).number_rankings_per_subject()

    def rankings(self):
        return rankings(results).number_rankings()

    def individual_subject_contribution(self,series):
        return contribution(results).individual_subject_contribution(series)

    def weak_students_contribution(self,grad):
        return contribution(results).weak_contribution(grad)

    def result(self):
        return results

    def corr_chem(self):
        chem = pd.DataFrame(round(self.result().corr().loc["Chemistry"][2:13],5))
        return chem.sort_values(ascending=False,by="Chemistry").iloc[1].name

    def corr_eng(self):
        eng = pd.DataFrame(round(self.result().corr().loc["English"][2:13], 5))
        return eng.sort_values(ascending=False, by="English").iloc[1].name

    def pass_percentage(self,subject):
        if subject in self.science_subjects:
            return (len(results.where(results[subject] >= 45).dropna())/len(results))*100
        else:
            return (len(results.where(results[subject] >= 55).dropna())/len(results))*100

    def std(self,subject):
        return round(results.describe().loc["std"][subject],1)
    def top_student(self,subject):
        max = results.describe().loc["max"]
        ind = [results[subject].values.tolist().index(y) for y in results[subject].values.tolist() if y == max[subject]][0]
        return results.iloc[ind]["Student Name"]

    def weighted(self):
        weight = [(results[subj].mean()*(self.number_of_subject_grades(subj)["A"]*self.pass_percentage(subj)))*0.002 for subj in self.subjects]
        ser = pd.Series(weight,index=self.subjects)
        dat = pd.DataFrame(ser.sort_values(ascending=False))
        blank = [self.teacher.teacher_list[name] for name in dat.index]
        dat["Teachers"] = blank
        dat["Subject"] = dat.index
        dat = dat[["Teachers","Subject",0]]
        return dat




