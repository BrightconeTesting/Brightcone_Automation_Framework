@echo off
echo Cleaning old reports...
if exist reports\allure-results del /q reports\allure-results\*
if exist reports\allure-report rmdir /s /q reports\allure-report

echo Running Behave tests...
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results

echo Generating Allure report...
echo NOTE: You MUST have the 'allure' command-line tool installed on your system to generate the HTML report.
echo Install it using: scoop install allure OR download manually from github.com/allure-framework/allure2
allure generate reports/allure-results --clean -o reports/allure-report

echo Opening report...
allure open reports/allure-report
