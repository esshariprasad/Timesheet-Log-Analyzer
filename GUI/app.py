# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog
import xlrd
import re
import xlwt
import json

global_Cat_Dict={} 
all_subjects_dict={}
TA_names={}
FinalCourses={}
CoordinatorCourseHours_dict={}


Debug=False
UserDebug=False


class TAWorkPerformed():
    
    def openSheet(self,inputsheet):
        
        #inputsheet
        loc = (inputsheet)
        self.wb = xlrd.open_workbook(loc)
        self.sheet = self.wb.sheet_by_index(0)

        #to get number of rows in the sheet
        self.sheet.num_rows = self.sheet.nrows 
        return self.sheet,self.sheet.num_rows

    def dataCheck(self):
            
        #place hours work cloumn un cellvalue(m,n ) in n places and check

        Work_Hours_each_cat=self.sheet.cell_value(2,self.sheet.HoursofWork_row_index)

        Work_Hours_each_cat=re.sub("\d\) ","",Work_Hours_each_cat)
        Work_Hours_each_cat=re.sub("\d\) ","",Work_Hours_each_cat)

        Work_Hours_each_cat=Work_Hours_each_cat.split(", ")
        
        if Debug==True:
            print(f'check whether taken input is of right column \n"{Work_Hours_each_cat}\n ====== \n')






    def CreatingOutputSheet(self):
        ##Creating output sheet
        newsheet=xlwt.Workbook()
        sheet1 = newsheet.add_sheet("TA work Performed Final")
        cols=['WorkPerformed','Hours']
        txt = "Row %s, Col %s"

        row = sheet1.row(0)
        row.write(0,'WorkPerformed')
        row.write(1,'Hours')

        index=1
        work_per=0
        Hours_per=1
        for key,value in global_Cat_Dict.items():
            
            row = sheet1.row(index)

            row.write(work_per,key)
            row.write(Hours_per,value)
            index=index+1

        # T=json.dumps(global_Cat_Dict)
        newsheet.save("TA work Performed.xls")
        

    def BuildingDict(self):
    #building global dict for each category
        for r in range(1,self.sheet.num_rows): 
            Work_Performed_ALL=self.sheet.cell_value(r, self.sheet.workperformed_row_index)
        
            Work_Performed_ALL=re.sub("\d\) ","",Work_Performed_ALL)
            Work_Performed_ALL=re.sub("\d","",Work_Performed_ALL)
            different_categories = Work_Performed_ALL.split(", ")
            # print(different_categories)
            # Creating dictionaries
            for i in different_categories:
                if i not in global_Cat_Dict: 
                    global_Cat_Dict[i]=0.0




    # print(global_Cat_Dict)
    #total activity count
    # print(len(global_Cat_Dict))


    def CategorySperator(self):
    #Builds list for each category using a List
    ## :: prints row number extracts the workperformed category for each row
    ## :: create a unquie hash map for each row

        for r in range(1,self.sheet.num_rows): 
            local_list=[]
            #print row number
            
            if UserDebug==True:
                print(f'rownumber={r+1}')   
            workperformed_row_index=self.sheet.workperformed_row_index
            HoursofWork_row_index=self.sheet.HoursofWork_row_index
            totalApporvedHours_row_index=self.sheet.totalApporvedHours_row_index

            Work_Performed_ALL=self.sheet.cell_value(r, workperformed_row_index)
            Work_Performed_ALL=re.sub("\d\) ","",Work_Performed_ALL)
            Work_Performed_ALL=re.sub("\d","",Work_Performed_ALL)
            different_categories = Work_Performed_ALL.split(", ")
            
            for i in different_categories:
            #add all without removing duplicates 
                    local_list.append(i)   
            


        

            
                
            workhour_list=[]
            #row looks like 1) 1.00, 2) 1.00, 3) 0.50
            #removes all the indexs from the work row but those are they key for us to add up the data attendance taking, attendance taking
            Work_Hours_each_cat=self.sheet.cell_value(r, HoursofWork_row_index)
            Work_Hours_each_cat=re.sub("\d*\) ","",Work_Hours_each_cat)
        
            Work_Hours_each_cat=Work_Hours_each_cat.split(", ")
            
            for i in Work_Hours_each_cat:
                    workhour_list.append(i) 

            #Debug statement:
            # prints hours for each row for each work category
            #Debug : 
            # print(workhour_list)
            
                    
            local_dict_combined={}
            
            #considers all the extracted column data in different categories
            for i in different_categories:
                if i not in local_dict_combined: 
                    #initializing each category for each row under zero
                    local_dict_combined[i]=0.0   

            
            check_Total_Course_hours=self.sheet.cell_value(r, totalApporvedHours_row_index)
            # print(check_Total_Course_hours)
            
            r_local_in_cell=0
            #prev for maintaing the lookup while considering the hours of working and work performed
            




            #debug:
            LV_check_total=0.0
            prev=[]
            #we use work performed row to look and utilize the workhour_list to add things
            
            for i in local_list:
                
                
                if(i in prev):
                    #DEBUG:
                    #activity already seen add up
                    # print(f'already seen this up')

                    local_dict_combined[i]=float(local_dict_combined[i])+float(workhour_list[r_local_in_cell])
                    
                    #debug:
                    LV_check_total=LV_check_total+float(workhour_list[r_local_in_cell])


                else:
                    
                    #activity not see add entry
                    #Debug statement
                    # print(f'index={i}')
                    #converting the worklist at each index 


                    local_dict_combined[i]=float(workhour_list[r_local_in_cell])
                    #appending the key
                    prev.append(i)

                    #debug:
                    LV_check_total=LV_check_total+float(workhour_list[r_local_in_cell])
                    # print(LV_check_total)

                # Debug statement
                # print(prev)   

                #adding up the index for workhour_list
                r_local_in_cell=r_local_in_cell+1


                #debug:
                # check for the total hours and local value
                # print(f'here={check_Total_Course_hours}')
                # m=float(check_Total_Course_hours)
                # print(m)
                # print(float(LV_check_total))
                
            if(float(check_Total_Course_hours)!=float(LV_check_total)):
                print(f'{check_Total_Course_hours} not equal to {LV_check_total}')
                    
                
                
                

                
            # print(local_dict_combined)

            #adding to total:
            for i in local_dict_combined:
                global_Cat_Dict[i]=global_Cat_Dict[i]+local_dict_combined[i]    
            # print(global_Cat_Dict)        







    def setupInputSheet(self,filepath):
        self.filepath=filepath
        

        print(self.filepath)
         




class CategoryForEachSubject():

    def openSheet(self,inputsheet):
        loc = (inputsheet)

        wb = xlrd.open_workbook(loc)

        self.sheet = wb.sheet_by_index(0)



        #to get number of rows in the sheet
        self.sheet.num_rows = self.sheet.nrows 
        return self.sheet,self.sheet.num_rows

    def buildFinalDic(self):

        workperformed_row_index=self.sheet.workperformed_row_index
        final_Dict={}
        # loc = (self.filepath)

        # wb = xlrd.open_workbook(loc)

        # sheet = wb.sheet_by_index(0)

        #to get number of rows in the sheet
        num_rows = self.sheet.nrows 
        workperformed_row_index=self.sheet.workperformed_row_index
      
        for r in range(1,num_rows): 
            Work_Performed_ALL=self.sheet.cell_value(r, workperformed_row_index)
        
            Work_Performed_ALL=re.sub("\d\) ","",Work_Performed_ALL)
            Work_Performed_ALL=re.sub("\d","",Work_Performed_ALL)
            different_categories = Work_Performed_ALL.split(", ")
            # print(different_categories)
            # Creating dictionaries
            for i in different_categories:
                if i not in final_Dict: 
                    final_Dict[i]=0.0

        
        return final_Dict

    def PrintToExcel(self):
        

        final_Dict=self.buildFinalDic()
        
        Reset_dict=final_Dict.copy()
        dict_input=all_subjects_dict

        # ##Creating output sheet
        newsheet=xlwt.Workbook()
        sheet1 = newsheet.add_sheet("TA work Performed")
        # cols=['Subject','Hours']
        

        row = sheet1.row(0)
        row.write(0,'Subject')
        worktype_index_col=1
        for worktype in final_Dict:

            row.write(worktype_index_col,worktype)
            worktype_index_col+=1

            
            

        
        row_number=1
        worktype_index_col=1
        for key in dict_input:
            
            subject=key
            row = sheet1.row(row_number)
            row_number+=1
            #wrting subject name
            row.write(0,subject)
            # print(f'{key}')

            #rest dict foe each subject
            final_Dict=Reset_dict.copy()
            for key2 in dict_input[subject]:
                
            
                work_performed=key2
                Time=dict_input[key][key2]
                
                final_Dict[work_performed]=Time
                # print(f'{key2} {dict_input[key][key2]}')
                
                
                
            
            # print( f'\n {subject}: \n {final_Dict} \n')
            
            for key in final_Dict:
                row.write(worktype_index_col,final_Dict[key])
                worktype_index_col+=1
            worktype_index_col=1
            
            

        newsheet.save("Categoryforeachsubject.xls") 

    def DataCheckup(self):
    # #place hours work cloumn un cellvalue(m,n ) in n places and check

    # #course number column


    # #work category column starting from row 2,9 (10th in excel)
        HoursofWork_row_index=self.sheet.HoursofWork_row_index
       

        Work_Hours_each_cat=self.sheet.cell_value(2, HoursofWork_row_index)

        Work_Hours_each_cat=re.sub("\d\) ","",Work_Hours_each_cat)
        Work_Hours_each_cat=re.sub("\d\) ","",Work_Hours_each_cat)

        Work_Hours_each_cat=Work_Hours_each_cat.split(", ")

        if Debug is True:
            print(f'check whether taken input is of right column \n"{Work_Hours_each_cat}\n ====== \n')

    ##---------------Data checkup ends------------------

    def buildAllSubjectsDict(self):
            
        for r in range(1,self.sheet.num_rows): 
            Coursename=self.sheet.cell_value(r,self.sheet.course_name_index)
            if Coursename not in all_subjects_dict:
                all_subjects_dict[Coursename]={}

    # print(all_subjects_dict)

    def CategorySeperator(self):

        totalApporvedHours_row_index=self.sheet.totalApporvedHours_row_index
        workperformed_row_index=self.sheet.workperformed_row_index
        HoursofWork_row_index=self.sheet.HoursofWork_row_index
        sheet=self.sheet
        num_rows=self.sheet.num_rows
        course_name_index=self.sheet.course_name_index

        for subject in all_subjects_dict:
            Cat_Dict={}
            for r in range(1,num_rows): 

                if subject in sheet.cell_value(r,course_name_index):
                    # print(f'{subject} is present at {r}')




                #building global dict for each category for each particular subject

                    

                    Work_Performed_ALL=sheet.cell_value(r, workperformed_row_index)
                
                    Work_Performed_ALL=re.sub("\d\) ","",Work_Performed_ALL)
                    Work_Performed_ALL=re.sub("\d","",Work_Performed_ALL)
                    different_categories = Work_Performed_ALL.split(", ")
                    # print(different_categories)
                    # Creating dictionaries
                    for i in different_categories:
                        if i not in Cat_Dict: 
                            Cat_Dict[i]=0.0

                    # print(global_Cat_Dict)
                    #total activity count
                    # print(len(global_Cat_Dict))


                    ## :: prints row number extracts the workperformed category for each row
                    ## :: create a unquie hash map for each row
                
                    local_list=[]
                    #print row number
                    # print(f'rownumber={r}')
                    Work_Performed_ALL=sheet.cell_value(r, workperformed_row_index)
                    Work_Performed_ALL=re.sub("\d\) ","",Work_Performed_ALL)
                    Work_Performed_ALL=re.sub("\d","",Work_Performed_ALL)
                    different_categories = Work_Performed_ALL.split(", ")
                    
                    for i in different_categories:
                    #add all without removing duplicates 
                            local_list.append(i)   
                    
                    #---  /* Debug statements:
                    # print('\n printing local list of each category')
                    # print(local_list)

                    # */---------

                    #implement in new python file to improve code structure  
                    # ##Creating output sheet
                    # newsheet=xlwt.Workbook()
                    # sheet1 = newsheet.add_sheet("TA each task")
                    # cols=['WorkPerformed','Hours']
                    # txt = "Row %s, Col %s"

                    # row = sheet1.row(0)
                    # row.write(0,'WorkPerformed')
                    # row.write(1,'Hours')   

                    
                        
                    workhour_list=[]
                    
                    #removes all the indexs from the work row but those are they key for us to add up the data attendance taking, attendance taking
                    Work_Hours_each_cat=sheet.cell_value(r, HoursofWork_row_index)
                    Work_Hours_each_cat=re.sub("\d*\) ","",Work_Hours_each_cat)
                
                    Work_Hours_each_cat=Work_Hours_each_cat.split(", ")
                    
                    for i in Work_Hours_each_cat:
                            workhour_list.append(i) 

                    #Debug statement:
                    # prints hours for each row for each work category
                    #Debug : 
                    # print(workhour_list)
                    
                            
                    local_dict_combined={}
                    
                    #considers all the extracted column data in different categories
                    for i in different_categories:
                        if i not in local_dict_combined: 
                            #initializing each category for each row under zero
                            local_dict_combined[i]=0.0   

                    
                    check_Total_Course_hours=sheet.cell_value(r, totalApporvedHours_row_index)
                    # print(check_Total_Course_hours)
                    
                    r_local_in_cell=0
                    #prev for maintaing the lookup while considering the hours of working and work performed
                    




                    #debug:
                    LV_check_total=0.0
                    prev=[]
                    #we use work performed row to look and utilize the workhour_list to add things
                    
                    for i in local_list:
                        
                        
                        if(i in prev):
                            #DEBUG:
                            #activity already seen add up
                            # print(f'already seen this up')

                            local_dict_combined[i]=float(local_dict_combined[i])+float(workhour_list[r_local_in_cell])
                            
                            #debug:
                            LV_check_total=LV_check_total+float(workhour_list[r_local_in_cell])


                        else:
                            
                            #activity not see add entry
                            #Debug statement
                            # print(f'index={i}')
                            #converting the worklist at each index 


                            local_dict_combined[i]=float(workhour_list[r_local_in_cell])
                            #appending the key
                            prev.append(i)

                            #debug:
                            LV_check_total=LV_check_total+float(workhour_list[r_local_in_cell])
                            # print(LV_check_total)

                        # Debug statement
                        # print(prev)   

                        #adding up the index for workhour_list
                        r_local_in_cell=r_local_in_cell+1


                        #debug:
                        # check for the total hours and local value
                        # print(f'here={check_Total_Course_hours}')
                        # m=float(check_Total_Course_hours)
                        # print(m)
                        # print(float(LV_check_total))
                        
                    if(float(check_Total_Course_hours)!=float(LV_check_total)):
                        print(f'{check_Total_Course_hours} not equal to {LV_check_total}')
                            
                        
                        
                        

                        
                    # print(f'{subject}  {local_dict_combined}')

                    #adding to total:
                    for i in local_dict_combined:
                        Cat_Dict[i]=Cat_Dict[i]+local_dict_combined[i]    
                    # print(global_Cat_Dict)        
                

                all_subjects_dict[subject] =Cat_Dict       



class TATotalHours():
    def openSheet(self,inputsheet):
    
        loc = (inputsheet)

        wb = xlrd.open_workbook(loc)

        self.sheet = wb.sheet_by_index(0)



        #to get number of rows in the sheet
        self.sheet.num_rows = self.sheet.nrows 
        return self.sheet,self.sheet.num_rows

    def buildTaDict(self):
        
        if Debug is True:
            print("TAName=",self.sheet.Ta_Name)
            print("CoureName=",self.sheet.CCName)
        

        for r in range(1,self.sheet.num_rows): 
            TA_name=self.sheet.cell_value(r, self.sheet.Ta_Name)
            TA_name=TA_name.lower()


            if TA_name not in TA_names:
                TA_names[TA_name]=0
            
        # print(TA_names)
        
        # return final_Dict

    def CourseHours(self):

       
        for r in range(1,self.sheet.num_rows): 
            
            TA_name=self.sheet.cell_value(r, self.sheet.Ta_Name)
            TA_name=TA_name.lower()
            course_hours=self.sheet.cell_value(r,self.sheet.totalApporvedHours_row_index)
            course_hours=float(course_hours)
            
            TA_names[TA_name]+=course_hours

            TA_names[TA_name]=round(TA_names[TA_name],2)

        
        if Debug is True:
            print(TA_names)





    def PrintToExcel(self):
        

        # ##Creating output sheet
        newsheet=xlwt.Workbook()
        sheet1 = newsheet.add_sheet("TA User Total Hours")
        # cols=['Subject','Hours']
        

        row = sheet1.row(0)
        row.write(0,'Name')
        row.write(1,'Total Hours')
        Name_col=0
        Hours_col=1
        Row_number=1

        Sorted_TA_Names = list(TA_names.keys())
        Sorted_TA_Names.sort()
        Sorted_TA_Names_dict = {i: TA_names[i] for i in Sorted_TA_Names}


        for TAName in Sorted_TA_Names_dict:
            row = sheet1.row(Row_number)
            row.write(Name_col,TAName.capitalize())
            row.write(Hours_col,TA_names[TAName])
            Row_number+=1

    
        

        newsheet.save("TA User TotalHours.xls") 


class FinalCourseHours():


    def openSheet(self,inputsheet):
    
        loc = (inputsheet)

        wb = xlrd.open_workbook(loc)

        self.sheet = wb.sheet_by_index(0)



        #to get number of rows in the sheet
        self.sheet.num_rows = self.sheet.nrows 
        return self.sheet,self.sheet.num_rows

    def buildFinalCoursesDict(self):
        '''takes taname column and '''

        if Debug is True:
            print("CoureNameCol=",self.sheet.course_name_index)
            
        

        for r in range(1,self.sheet.num_rows): 
            CourseName=self.sheet.cell_value(r, self.sheet.course_name_index)
            CourseName=CourseName.lower()


            if CourseName not in FinalCourses:
                FinalCourses[CourseName]=0

        if Debug is True:    
            print(FinalCourses)  
            print(len(FinalCourses))  
        
        # return final_Dict

    def ComputeCourseHours(self):

       
        for r in range(1,self.sheet.num_rows): 
            
            CourseName=self.sheet.cell_value(r, self.sheet.course_name_index)
            CourseName=CourseName.lower()
            course_hours=self.sheet.cell_value(r,self.sheet.totalApporvedHours_row_index)
            course_hours=float(course_hours)
            
            FinalCourses[CourseName]+=course_hours

            FinalCourses[CourseName]=round(FinalCourses[CourseName],2)

        
        if Debug is True:
            print(FinalCourses) 

           

         





    def PrintToExcel(self):
        

        # ##Creating output sheet
        newsheet=xlwt.Workbook()
        sheet1 = newsheet.add_sheet("Final Course Hours")
        # cols=['Subject','Hours']
        

        row = sheet1.row(0)
        row.write(0,'Course Name')
        row.write(1,'Total Course Hours')
        CourseName_colno=0
        TotalCourseHours_colno=1
        Row_number=1

        Sorted_FinalCourses = list(FinalCourses.keys())
        Sorted_FinalCourses.sort()
        Sorted_FinalCourses_dict = {i: FinalCourses[i] for i in Sorted_FinalCourses}


        for CourseName in Sorted_FinalCourses_dict:
            row = sheet1.row(Row_number)
            row.write(CourseName_colno,CourseName.capitalize())
            row.write(TotalCourseHours_colno,FinalCourses[CourseName])
            Row_number+=1

    
        

        newsheet.save("Final Course Hours.xls") 


class CoordinatorCourseHours():


    def openSheet(self,inputsheet):
    
        loc = (inputsheet)

        wb = xlrd.open_workbook(loc)

        self.sheet = wb.sheet_by_index(0)



        #to get number of rows in the sheet
        self.sheet.num_rows = self.sheet.nrows 
        return self.sheet,self.sheet.num_rows

    def buildCoordinatorCourseHoursDict(self):
        '''takes taname column and '''

        if Debug is True:
            print("CoureNameCol=",self.sheet.course_name_index)
            
        for coursename in FinalCourses:
            

            CoordinatorCourseHours_dict[coursename]={}
            

        for r in range(1,self.sheet.num_rows): 
            CourseName=self.sheet.cell_value(r, self.sheet.course_name_index)
            CourseName=CourseName.lower()
            Coordinator_name= self.sheet.cell_value(r,self.sheet.CCName)

            if Coordinator_name not in CoordinatorCourseHours_dict[CourseName]:
                CoordinatorCourseHours_dict[CourseName][Coordinator_name.lower()]=0

          
        if Debug is True:    
            print(CoordinatorCourseHours_dict)  


    def ComputeCourseHours(self):

        
        for r in range(1,self.sheet.num_rows): 
            CourseName=self.sheet.cell_value(r, self.sheet.course_name_index)
            CourseName=CourseName.lower()
            Coordinator_name= self.sheet.cell_value(r,self.sheet.CCName)
            Coordinator_name=Coordinator_name.lower()
            course_hours=self.sheet.cell_value(r,self.sheet.totalApporvedHours_row_index)
            course_hours=float(course_hours)
            
            CoordinatorCourseHours_dict[CourseName][Coordinator_name]+=course_hours

            CoordinatorCourseHours_dict[CourseName][Coordinator_name]=round(CoordinatorCourseHours_dict[CourseName][Coordinator_name],2)

        if Debug is True:   
            print(CoordinatorCourseHours_dict)    

     

    def PrintToExcel(self):
        

        # ##Creating output sheet
        newsheet=xlwt.Workbook()
        sheet1 = newsheet.add_sheet("Cordinator Course Hours")
        # cols=['Subject','Hours']
        

        row = sheet1.row(0)
        row.write(0,'Course Name')
        row.write(1,'Hours')
        CourseName_colno=0
        CoordinatorName_colno=0
        TotalCourseHours_colno=1
        Row_number=1

        Sorted_CoordinatorCourseHours_dict = list(CoordinatorCourseHours_dict.keys())
        Sorted_CoordinatorCourseHours_dict.sort()
        Sorted_CoordinatorCourseHours_dict = {i: CoordinatorCourseHours_dict[i] for i in Sorted_CoordinatorCourseHours_dict}


        for CourseName in Sorted_CoordinatorCourseHours_dict:
            row = sheet1.row(Row_number)
            row.write(CourseName_colno,CourseName.capitalize())
            row.write(TotalCourseHours_colno,FinalCourses[CourseName])
            Row_number+=1
            # Coordinator hours:
            for Coordinatorname in Sorted_CoordinatorCourseHours_dict[CourseName]:
                
                row = sheet1.row(Row_number)
        
                row.write(CoordinatorName_colno,Coordinatorname.capitalize())
                
                row.write(TotalCourseHours_colno,Sorted_CoordinatorCourseHours_dict[CourseName][Coordinatorname])
                Row_number+=1

            Row_number+=2   

    
        

        newsheet.save("Cordinator Course Hours.xls") 


         
        


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1005, 713)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(130, 50, 113, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 10, 151, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 50, 91, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(430, 50, 113, 21))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(290, 50, 131, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(130, 120, 113, 21))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 120, 111, 20))
        self.label_5.setObjectName("label_5")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_8.setGeometry(QtCore.QRect(430, 120, 113, 21))
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(290, 120, 121, 16))
        self.label_8.setObjectName("label_8")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget,clicked=lambda: self.upload())
        self.pushButton.setGeometry(QtCore.QRect(140, 290, 161, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget,clicked=lambda: self.submit())
        self.pushButton_2.setGeometry(QtCore.QRect(430, 290, 161, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(20, 540, 111, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(749, 670, 231, 20))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(140, 540, 561, 16))
        self.label_11.setObjectName("label_11")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(130, 180, 113, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(430, 180, 113, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 180, 60, 16))
        self.label_3.setObjectName("label_3")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(290, 180, 121, 16))
        self.label_6.setObjectName("label_6")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "COPIT TA Time Sheet Tool"))
        self.lineEdit.setText(_translate("MainWindow", "5"))
        self.label.setText(_translate("MainWindow", "Column Set up"))
        self.label_2.setText(_translate("MainWindow", "Course Name"))
        self.lineEdit_4.setText(_translate("MainWindow", "8"))
        self.label_4.setText(_translate("MainWindow", "Work Performed"))
        self.lineEdit_5.setText(_translate("MainWindow", "10"))
        self.label_5.setText(_translate("MainWindow", "Hours of Work"))
        self.lineEdit_8.setText(_translate("MainWindow", "11"))
        self.label_8.setText(_translate("MainWindow", "Total Course Hours"))
        self.pushButton.setText(_translate("MainWindow", "Upload Excel Sheet"))
        self.pushButton_2.setText(_translate("MainWindow", "Submit"))
        self.label_9.setText(_translate("MainWindow", "File Source"))
        self.label_10.setText(_translate("MainWindow", "Created by: Sai Shiva Hari Prasad"))
        self.label_11.setText(_translate("MainWindow", "None"))
        self.lineEdit_2.setText(_translate("MainWindow", "1"))
        self.lineEdit_3.setText(_translate("MainWindow", "6"))
        self.label_3.setText(_translate("MainWindow", "Name"))
        self.label_6.setText(_translate("MainWindow", "Coordinator Name"))

    def IntitializeColumns(self):

        self.sheet.workperformed_row_index=int(self.lineEdit_4.text())-1
        
        #looks like start from zero index
        #1) Attendance - TAKING, 2) Attendance - TAKING, 3) Answering e-mails

        self.sheet.HoursofWork_row_index=int(self.lineEdit_5.text())-1
        # 1) 1.00, 2) 1.00, 3) 0.50

        self.sheet.totalApporvedHours_row_index=int(self.lineEdit_8.text())-1
       
        self.sheet.course_name_index=int(self.lineEdit.text())-1

       

        #Course Coordinator Name
        self.sheet.CCName= int(self.lineEdit_3.text())-1

        #TA name
        self.sheet.Ta_Name= int(self.lineEdit_2.text())-1


        
    def CompileSheets(self):
        

        # TAWork Performed
        TWP=TAWorkPerformed()
        # TWP.setupInputSheet(self.filepath)
        self.sheet,self.sheet.num_rows=TWP.openSheet(self.filepath)
        self.IntitializeColumns()

        if UserDebug is True: 
            print(self.sheet,self.sheet.num_rows)
        
        TWP.dataCheck()
        TWP.BuildingDict()
        TWP.CategorySperator()


        # Creating instance again it will lose all its inherent properties
        # Catefory for Each Subject Sheet generation
        CFES=CategoryForEachSubject()
        self.sheet,self.sheet.num_rows=CFES.openSheet(self.filepath)
        if UserDebug is True: 
            print(self.sheet,self.sheet.num_rows)

        self.IntitializeColumns()
        CFES.DataCheckup()
        CFES.buildAllSubjectsDict()
        CFES.CategorySeperator()
     

       

        # Creating instance again it will lose all its inherent properties
        # Catefory for Each Subject Sheet generation
        TTS= TATotalHours()
        self.sheet,self.sheet.num_rows=TTS.openSheet(self.filepath)

        #intialize cloumns()

         # TA name
      
        self.IntitializeColumns()
        TTS.buildTaDict()
        TTS.CourseHours()

        FCH=FinalCourseHours()
        self.sheet,self.sheet.num_rows=FCH.openSheet(self.filepath)
        self.IntitializeColumns()
        FCH.buildFinalCoursesDict()
        FCH.ComputeCourseHours()

        CCH=CoordinatorCourseHours()
        self.sheet,self.sheet.num_rows=CCH.openSheet(self.filepath)
        self.IntitializeColumns()
        CCH.buildCoordinatorCourseHoursDict()
        CCH.ComputeCourseHours()

        


      
        
        
     

       
        

        



    def upload(self):
        
        fullPath = QFileDialog.getOpenFileName(self.centralwidget,"Open File", "../", "All Files (*)")
        # fname = QFileDialog.getOpenFileName(self, "Open File", "./test_images/", "All Files (*)")
      
        self.filepath=fullPath[0]

      
        #file path input is done here

        print(self.filepath)
        print("\n Current Column Setup")

        print(self.lineEdit.text(),self.lineEdit_4.text(),self.lineEdit_5.text(),self.lineEdit_8.text(),self.lineEdit_2.text(),self.lineEdit_3.text())

        self.label_11.setText(self.filepath)


        


    def submit(self):
        
        print("Submit Setup:")
        print(self.lineEdit.text(),self.lineEdit_4.text(),self.lineEdit_5.text(),self.lineEdit_8.text(),self.lineEdit_2.text(),self.lineEdit_3.text())

        self.CompileSheets()

        TWP=TAWorkPerformed()
        TWP.CreatingOutputSheet()

        CFES=CategoryForEachSubject()


        self.sheet,self.sheet.num_rows=CFES.openSheet(self.filepath)

        self.sheet.workperformed_row_index=int(self.lineEdit_4.text())-1
        
        #looks like start from zero index
        #1) Attendance - TAKING, 2) Attendance - TAKING, 3) Answering e-mails

        self.sheet.HoursofWork_row_index=int(self.lineEdit_5.text())-1
        # 1) 1.00, 2) 1.00, 3) 0.50

        self.sheet.totalApporvedHours_row_index=int(self.lineEdit_8.text())-1
       
        #looks like start from zero index
        #1) Attendance - TAKING, 2) Attendance - TAKING, 3) Answering e-mails

      
        # 1) 1.00, 2) 1.00, 3) 0.50

        

        self.sheet.course_name_index=int(self.lineEdit.text())-1

        CFES.PrintToExcel()

        TTS= TATotalHours()
        TTS.PrintToExcel()

        FCH= FinalCourseHours()
        FCH.PrintToExcel()

        CCH=CoordinatorCourseHours()
        CCH.PrintToExcel()

        print("All Sheets Generated")
        

        
        
             # CreatingOutputSheet()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())