IR Project:
Goal: Design and build your own information retrieval systems, evaluate and compare their performance in terms of retrieval effectiveness.

CITATION: Third party python libraries used
1) BeautifulSoup
2) numpy
3) scipy
4) nltk

INSTALLATION GUIDE:
-- Download python 2.7.x from https://www.python.org/download/releases/2.7/
-- From Windows Home go to Control Panel -> System and Security -> System -> Advanced System Settings -> Environment Variables and add two new variables in 'PATH' -> [Home directory of Python]; [Home directory of Python]\Scripts
-- Open Command Prompt and upgrade pip using the following command: 'python -m pip install -U pip'
-- To check whether you have pip installed properly, just open the command prompt and type 'pip'
-- It should not throw an error, rather details regarding pip will be displayed.
-- Install BeautifulSoup by using the command 'pip install beautifulsoup4'
-- If for some reason the installation fails due to the absence of certain package, just install that package using 'pip install name_of_that_package'
-- Open the unzipped folder and open a command prompt in that location and write the given command - 'C:\Python27\python.exe setup.py install'

-- Install JAVA SE6 or above if not already installed in the system from http://www.oracle.com/technetwork/java/javase/index-137561.html#windows
-- From Windows Home go to Control Panel -> System and Security -> System -> Advanced System Settings -> Environment Variables and add new variable in 'PATH' -> [Home directory of Java]\jdk[version number]\bin;


INSTRUCTIONS:

PHASE1: Indexing and Retrieval
TASK 1, 2 and 3:
You can run these tasks by inputting "python main.py" into the console.
We have incorporated user input to run each Task to make it easier for the user to perform the task he desires.
The console will ask you to input 1, 2 or 3 and each of these numbers signify which task number needs to be performed.
If you enter 1, it will ask you to run Task1 TFIDF or BM25 by entering a or b. Same goes with Task 2 (Pseudo relevance).
If you want to run Task 1 Lucene then you will need to go into the directory where the file LuceneImplementation.java resides.
Then run it using commands "javac LuceneImplementation.java", "java LuceneImplementation"
(NOTE:  1) Make sure query_file.txt is in the same project folder where the Java file is stored in directory of IDE.
	2) Make sure the necessary jar files (provided in HW4) are added to the IDE you are using. If this jar files aren't added Lucene won't work.
	3) Output file of Lucene run “Task_1_Lucene.txt” will get generated in the workspace folder of the project in which the Java file resides for the IDE used)

When you enter 3 to perform task 3 it will ask you to enter either "a" or "b" ("a" for Task_3a i.e. Stopping, "b" for Task_3b i.e. Stemming)
And then it will ask you use enter a or b for the retrieval model, TFIDF or BM25, you want to use.

The output is the ranked tables for all these system runs. But we already performed the whole process once for each query for the graders convenience and the ranked files reside in the directory "Phase_1_Output".


PHASE2: Evaluation
You can run the evaluation process by entering "python Evaluation.py" into the console.
The program will calculate the evaluation measures for each of the file names that reside in the "files" list variable. If you wish to perform evaluation on other ranked lists then you would have to make changes to that "files" variable.
Once the user enters the correct file name, the program will create 3 files: "FILENAME_precision_recall.txt", "FILENAME_p@5.txt", "FILENAME_p@20.txt".
1) MAP of the system is written into the MAP_of_models.txt file.
2) MRR of the system is written into the MRR_of_models.txt file. 
3) P@5, P@20 are written in the files "....._p@5.txt" "....._p@20.txt".
4) Precision & Recall are displayed in a tabular format in the files "...._precision_recall.txt". The last 2 values in each line of the file are the Precision and Recall values respectively.

We have already run Evaluation.py on all the systems and all their outputs reside in the "Phase_2_Output" directory. 

Also, all .xls files for each of the seven systems (excluding stemming TFIDF and BM25) are provided in “Spreadsheet_Output” folder with all the information for your convenience.


BONUS TASK:
To run t-test, enter “python T-Test.py”. It will create a directory “Bonus_tasks_Output” with the comparisons of the values.
Also, .xlsx file for t-test results is provided in “Bonus_tasks_Output” folder.
To run snippet generation, enter “python SnippetGeneration.py” in the console. 
The program will create a “Snippet_Corpus” folder with all cacm files and a “Snippets.txt” file inside “Bonus_tasks_Output” folder which includes the snippet generated for top 10 cacm files retrieved for a given query using BM25_stopping with the query terms highlighted within <b><\b> tag in the snippet, ignoring stop words.






