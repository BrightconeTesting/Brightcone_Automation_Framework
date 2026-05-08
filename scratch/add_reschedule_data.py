import openpyxl
import os

file_path = r'c:\Users\Dell\OneDrive\Desktop\Bright_Automation_Before_Adding_Session\testdata\excel\recruitment_data.xlsx'
wb = openpyxl.load_workbook(file_path)
sheet = wb.active

new_row = [
    'Re-schedule interview slot and verify status', # scenario
    'admin', # role
    None, # file_name
    'Reschedule', # expected_result (for status validation)
    None, # category
    'QA Engineer', # job_role
    None, # resume_name
    None, # source
    None, # google_drive_link
    None, # candidate_name
    'May 8, 2026 08:00 AM', # start_date
    'May 8, 2026 09:00 AM', # end_date
    'Test Interviewer', # interviewer_name
    None, # from_date
    None, # to_date
    None, # interviewer_mail
    None  # slot_duration
]

sheet.append(new_row)
wb.save(file_path)
print("Data appended successfully.")
