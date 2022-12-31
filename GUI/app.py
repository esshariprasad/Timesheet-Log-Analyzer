# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app-new.ui'
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



class TAWorkPerformed():
    
    def openSheet(self):
        
        #inputsheet
        loc = (self.filepath)
        self.wb = xlrd.open_workbook(loc)
        self.sheet = self.wb.sheet_by_index(0)

        #to get number of rows in the sheet
        self.sheet.num_rows = self.sheet.nrows 
        return self.sheet,self.sheet.num_rows

    def dataCheck(self):
            
        #place hours work cloumn un cellvalue(m,n ) in n places and check

        Work_Hours_each_cat=self.sheet.cell_value(2, 9)

        Work_Hours_each_cat=re.sub("\d\) ","",Work_Hours_each_cat)
        Work_Hours_each_cat=re.sub("\d\) ","",Work_Hours_each_cat)

        Work_Hours_each_cat=Work_Hours_each_cat.split(", ")
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
            Work_Performed_ALL=self.sheet.cell_value(r, 7)
        
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
            # print(f'rownumber={r}')
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

        # print(final_Dict)
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
        print(f'check whether taken input is of right column \n"{Work_Hours_each_cat}\n ====== \n')

    ##---------------Data checkup ends------------------

    def buildAllSubjectsDict(self):
            
        for r in range(1,self.sheet.num_rows): 
            Coursename=self.sheet.cell_value(r,4)
            if Coursename not in all_subjects_dict:
                all_subjects_dict[Coursename]={}

    # print(all_subjects_dict)

    def CategorySeperator(self):

        totalApporvedHours_row_index=self.sheet.totalApporvedHours_row_index
        workperformed_row_index=self.sheet.workperformed_row_index
        HoursofWork_row_index=self.sheet.HoursofWork_row_index
        sheet=self.sheet
        num_rows=self.sheet.num_rows

        for subject in all_subjects_dict:
            Cat_Dict={}
            for r in range(1,num_rows): 

                if subject in sheet.cell_value(r,4):
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





class Ui_MainWindow(object):


    def CompileSheets(self):
        

        # TAWork Performed
        TWP=TAWorkPerformed()
        TWP.setupInputSheet(self.filepath)
        self.sheet,self.sheet.num_rows=TWP.openSheet()
           #all indexs start from zero
        self.sheet.workperformed_row_index=7
        #looks like start from zero index
        #1) Attendance - TAKING, 2) Attendance - TAKING, 3) Answering e-mails

        self.sheet.HoursofWork_row_index=9
        # 1) 1.00, 2) 1.00, 3) 0.50

        self.sheet.totalApporvedHours_row_index=10
        # 3 -- represents the approved usally lesser number
        print(self.sheet,self.sheet.num_rows)
       
        
     

        TWP.dataCheck()
        TWP.BuildingDict()
      
        
        TWP.CategorySperator()
        CFES=CategoryForEachSubject()
        self.sheet,self.sheet.num_rows=CFES.openSheet(self.filepath)

        print(self.sheet,self.sheet.num_rows)

        self.sheet.workperformed_row_index=7
        #looks like start from zero index
        #1) Attendance - TAKING, 2) Attendance - TAKING, 3) Answering e-mails

        self.sheet.HoursofWork_row_index=9
        # 1) 1.00, 2) 1.00, 3) 0.50

        self.sheet.totalApporvedHours_row_index=10
        CFES.DataCheckup()
        CFES.buildAllSubjectsDict()
        CFES.CategorySeperator()
        
        print(all_subjects_dict)

    #         sheet,num_rows=openSheet(inputsheet)
    # # DataCheckup(sheet,HoursofWork_row_index)
    # buildAllSubjectsDict(sheet,num_rows)
    # CategorySeperator(sheet,num_rows,workperformed_row_index,HoursofWork_row_index,totalApporvedHours_row_index)
    # PrintToExcel(all_subjects_dict,workperformed_row_index)



        # print(global_Cat_Dict)        
   



    def upload(self):
        
        fullPath = QFileDialog.getOpenFileName(self.centralwidget,"Open File", "../", "All Files (*)")
        # fname = QFileDialog.getOpenFileName(self, "Open File", "./test_images/", "All Files (*)")
      
        self.filepath=fullPath[0]

      
        #file path input is done here

        print(self.filepath)
        self.label_11.setText(self.filepath)

        self.CompileSheets()


    def submit(self):
        
        TWP=TAWorkPerformed()
        TWP.CreatingOutputSheet()

        CFES=CategoryForEachSubject()


        self.sheet,self.sheet.num_rows=CFES.openSheet(self.filepath)
        self.sheet.workperformed_row_index=7
        #looks like start from zero index
        #1) Attendance - TAKING, 2) Attendance - TAKING, 3) Answering e-mails

        self.sheet.HoursofWork_row_index=9
        # 1) 1.00, 2) 1.00, 3) 0.50

        self.sheet.totalApporvedHours_row_index=10
        CFES.PrintToExcel()
        
             # CreatingOutputSheet()

    

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
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(390, 50, 113, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(270, 50, 121, 20))
        self.label_3.setObjectName("label_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(800, 50, 113, 21))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(630, 50, 131, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(390, 130, 113, 21))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(270, 130, 111, 20))
        self.label_5.setObjectName("label_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_6.setGeometry(QtCore.QRect(140, 130, 113, 21))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(10, 130, 111, 16))
        self.label_6.setObjectName("label_6")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_8.setGeometry(QtCore.QRect(800, 120, 113, 21))
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(640, 120, 121, 16))
        self.label_8.setObjectName("label_8")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget,clicked=lambda: self.upload())
        self.pushButton.setGeometry(QtCore.QRect(140, 290, 161, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget,clicked=lambda: self.submit())
        self.pushButton_2.setGeometry(QtCore.QRect(430, 290, 161, 32))
        self.pushButton_2.setObjectName("pushButton_2",)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(130, 190, 113, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(20, 190, 91, 16))
        self.label_7.setObjectName("label_7")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(20, 540, 111, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(749, 670, 231, 20))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(140, 540,700 , 20))
        self.label_11.setObjectName("label_11")
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
        self.lineEdit_3.setText(_translate("MainWindow", "6"))
        self.label_3.setText(_translate("MainWindow", "Coordinator Name"))
        self.lineEdit_4.setText(_translate("MainWindow", "8"))
        self.label_4.setText(_translate("MainWindow", "Work Performed"))
        self.lineEdit_5.setText(_translate("MainWindow", "10"))
        self.label_5.setText(_translate("MainWindow", "Hours of Work"))
        self.lineEdit_6.setText(_translate("MainWindow", "9"))
        self.label_6.setText(_translate("MainWindow", "Work Description"))
        self.lineEdit_8.setText(_translate("MainWindow", "11"))
        self.label_8.setText(_translate("MainWindow", "Total Course Hours"))
        self.pushButton.setText(_translate("MainWindow", "Upload Excel Sheet"))
        self.pushButton_2.setText(_translate("MainWindow", "Submit"))
        self.lineEdit_2.setText(_translate("MainWindow", "1"))
        self.label_7.setText(_translate("MainWindow", "Name"))
        self.label_9.setText(_translate("MainWindow", "File Source"))
        self.label_10.setText(_translate("MainWindow", "Created by: Sai Shiva Hari Prasad"))
        self.label_11.setText(_translate("MainWindow", "None"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())