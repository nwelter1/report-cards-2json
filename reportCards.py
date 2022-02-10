from cgi import test
import csv
import pprint
pp = pprint.PrettyPrinter(indent=4)
class GenerateReport:
    def __init__(self, courses, marks, students, tests):
        self.courses = self.generate_ids(courses)
        self.marks = self.generate_marks(marks)
        self.students = self.generate_ids(students)
        self.tests = self.generate_ids(tests)
    
    # generating python dicts for all csv records containing an 'id' field
    def generate_ids(self, file):
        with open(file) as f:
            csv_reader = csv.reader(f, delimiter=',')
            line_count = 0
            keys = []
            courses = []
            clean_list = []
            d = {}
            for record in csv_reader:
                if line_count == 0:
                    keys = record
                else:
                    courses.append(record)
                line_count += 1
            for i in range(len(courses)):
                temp_d = dict(zip(keys, courses[i]))
                clean_list.append(temp_d)
            for i in range(len(clean_list)):
                d[clean_list[i]['id']] = clean_list[i]
        return d
    # generating python dicts for all csv records containing a 'test_id' field
    def generate_marks(self, file):
        with open(file) as f:
            csv_reader = csv.reader(f, delimiter=',')
            line_count = 0
            keys = []
            tests = []
            clean_list = []
            d = {}
            for record in csv_reader:
                if line_count == 0:
                    keys = record
                else:
                    tests.append(record)
                line_count += 1
            for i in range(len(tests)):
                    temp_d = dict(zip(keys, tests[i]))
                    clean_list.append(temp_d)
            for i in range(len(clean_list)):
                if clean_list[i]['student_id'] in d:
                    d[clean_list[i]['student_id']].append(clean_list[i])
                else:
                    d[clean_list[i]['student_id']] = [clean_list[i]]
            # pp.pprint(d)
            return d
    def test2Course(self):
        test_2_course = {}
        for test_id in self.tests:
            course_id = self.tests[test_id]['course_id']
            if course_id not in test_2_course:
                test_2_course[course_id] = self.courses[course_id]['name']
        return test_2_course
    
    def getCourse(self,test_id):
        courses = self.test2Course()
        return courses[test_id]
    
            

    def checkTestWeights(self):
        weight_totals = {}
        weight_check = []
        for test in self.tests.values():
            if test['course_id'] in weight_totals:
                weight_totals[test['course_id']] += int(test['weight'])
            else:
                weight_totals[test['course_id']] = int(test['weight'])
        for key in weight_totals:
            if weight_totals[key] != 100:
                print(self.courses[key])
                # weight_check.add(self.courses[key])
                print(f'{self.courses[key]["teacher"]}\'s tests have a weight of {weight_totals[key]}. Please adjust to 100 before moving on.')
        if not len(weight_check):
            return
        else:
            print('All courses are weighted properly!')

    def reportCards(self):
        output = {'students':[]}
        for student in self.students.values():
            id = student['id']
            name =  student['name']
            s_dict = {}
            s_dict['id'] = id
            s_dict['name'] = name
            s_dict['totalAverage'] = 0
            s_dict['courses'] = []
            print(s_dict)
        # for student in self.marks:
        #     averages = []
        #     if student in self.marks:
        #         for scores in self.marks:










report = GenerateReport('courses.csv', 'marks.csv','students.csv','tests.csv')
# pp.pprint(report.students)
# pp.pprint(report.marks)
# report.checkTestWeights()
# report.reportCards()
report.getCourse('1')
