Requirements:
- Python 2.7 https://www.python.org/ftp/python/2.7.13/python-2.7.13.msi
- pip (Python package manager)
- selenium (Used for browser automation)
- webdriver (chrome webdriver is included in chromedriver.zip)

Installing Guide:

1. Python 2.7
	1.1 Download https://www.python.org/ftp/python/2.7.13/python-2.7.13.msi (This is for Windows, for other platforms please see https://www.python.org/downloads/)
	1.2	Install Python
	1.3 Add Python to path variables if nessary
		1.3.1 On Windows right click on "Computer" and click on properties
		1.3.2 Click "Advanced system settings"
		1.3.3 Click "Environment Variables"
		1.3.4 Edit "Path" variable and add the path to where Python was installed. (Usually the path is "C:\Python27")
	1.4 Test if Python is installed by running "python" in the command window
	1.4.1 The Python interpreter should show up
	
2. Pip
	2.1.a If you already have Pip install you can skip this step.
	2.1.b If you do not have it installed continue to step 2.2
	2.2 Open the folder "get_pip" in the Tests directory
	2.3 Run the command "python get-pip.py" in that folder. This should install pip

3. selenium
	3.1	Open a command line and run the command "pip install -U selenium"
	
4. selenium requires a webdriver to control a web browser. The chromedriver is included in the Tests\chromedriver.zip
	4.1 Unzip the chromedriver to the Tests directory
	4.2 Other browser drivers are available at http://www.seleniumhq.org/download/
	
	
Runing Tests:
	1. Database test:
		1.1 Open command window and run the command "python test_database.py"
		1.2 Successful test run will result in a similar output:
			
			Ran 4 tests in 0.073s

			OK
	
		1.3 These test cases test for json formatting errors, all category has at least 5 questions, 
			each question must have 1 right answer, at least 4 wrong answers for multiple choice, 
			and check that there is very little probability that the wrong answers are similar 
			to the actual answer
	
	2. Black box test:
		1.1 Open command window and run the command "python test_database.py"
		
		1.3 Test if game loads
		1.4 More test cases to come.