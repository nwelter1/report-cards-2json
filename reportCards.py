from cgi import test
import csv
import pprint
from turtle import st
import json
pp = pprint.PrettyPrinter(indent=4)
class GenerateReport:
    def __init__(self, courses, marks, students, tests):
        self.courses = self.process_ids(courses)
        self.marks = self.process_marks(marks)
        self.students = self.process_ids(students)
        self.tests = self.process_ids(tests)
        self.test_course = self.testCourseMerge()
    
    # generating python dicts for all csv records containing an 'id' field
    def process_ids(self, file):
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
    def process_marks(self, file):
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
    # Joining tests and courses for easier analysis later on
    def testCourseMerge(self):
        test_2_course = {}
        for test_id in self.tests:
            weight = self.tests[test_id]['weight']
            course_id = self.tests[test_id]['course_id']
            teacher = self.courses[course_id]['teacher']
            name = self.courses[course_id]['name']
            test_2_course[test_id] = [course_id, name, teacher, weight]
        return test_2_course
    # checking to see if there are any classes that are weighted incorrectly
    def checkTestWeights(self):
        weight_totals = {}
        incorrect_weights = []
        for test in self.tests.values():
            if test['course_id'] in weight_totals:
                weight_totals[test['course_id']] += int(test['weight'])
            else:
                weight_totals[test['course_id']] = int(test['weight'])
        for key, total in weight_totals.items():
            if total != 100:
                incorrect_weights.append(self.courses[key])
                print(f'{self.courses[key]["teacher"]}\'s tests have a weight of {total}. Please adjust to 100 before moving on.')
        if not len(incorrect_weights):
            return True
        return False 

    def reportCards(self):
        output = {'students':[]}
        for student in self.students.values():
            id = student['id']
            name =  student['name']
            s_dict = {}
            s_dict['id'] = id
            s_dict['name'] = name
            s_dict['courses'] = self.generateCourseReport(id)
            print(f'courses = {s_dict["courses"]}')
            s_dict['totalAverage'] = self.calculateTotalAverage(s_dict['courses'])
            print(s_dict['courses'])
            output['students'].append(s_dict)
        return output
    def generateCourseReport(self, id):
        student_courses = []
        final_grades = self.calculateAverageClass(id)
        for course_id in final_grades:
            class_dict = {}
            class_dict['id'] = course_id
            class_dict['name'] = self.courses[course_id]['name']
            class_dict['teacher'] = self.courses[course_id]['teacher']
            class_dict['courseAverage'] = final_grades[course_id]
            student_courses.append(class_dict)
        return student_courses
    

    def calculateTotalAverage(self, courses):
        '''
        Method to calculated a total grade average based on 
        a list of dictionaries containing course info
        Method loops over each course that student took, finds their average grade,
        then averages into one final grade based on marks/number of classes taken
        '''
        total = 0
        count = 0
        for grade in courses:
            total += grade['courseAverage']
            count += 1
        return total/count

    def calculateAverageClass(self,student_id):
        '''
        method looks at all grades in a given students list of marks
        finds the test_id in each 
        '''
        results = {}
        for grade in self.marks[student_id]:
            test_id = grade['test_id']
            course_id = self.test_course[test_id][0]
            mark = int(grade['mark'])/100
            weight = int(self.test_course[test_id][3])
            test_score = round(mark*weight,1)

            # adding weights into full class avg
            if course_id in results:
                results[course_id] += test_score
            else:
                results[course_id] = test_score

        return results

# driver code
def run(courses, marks, students, tests):
    report = GenerateReport(courses, marks, students, tests)
    if not report.checkTestWeights():
        return 
    with open('test.json', 'w') as f:
        json.dump(report.reportCards(), f)
    print('Successfully wrote report cards to JSON!')
# run the driver code
#run('courses.csv', 'marks.csv','students.csv','tests.csv')


