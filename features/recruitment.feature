@Recruitment
Feature: Resume Management in Recruitment Module
  I want to add candidates and upload resumes for specific job roles,

  @Recruitment_Possitive
  Scenario: Add a resume for ML Engineer role
<<<<<<< HEAD
    Given I am logged into the application
    Then I should be on the "Dashboard" page
    When I navigate to Recruitment module
    Then I should be on the "Recruitment" page
    When I click on continue button of ML engineer role
    Then I should be on the "Overview" page
    When I click on "Add Candidate" or "Upload Resume"
    And I upload a valid resume file
    Then the resume should be uploaded successfully
    And the candidate should be listed under the ML Engineer role

  @Recruitment_Negative
  Scenario: Upload resume with unsupported file format
    Given I am logged into the application
    Then I should be on the "Dashboard" page
    When I navigate to Recruitment module
    Then I should be on the "Recruitment" page
    When I click on continue button of ML engineer role
    Then I should be on the "Overview" page
    When I click on "Add Candidate" or "Upload Resume"
    And I upload a Invalid resume file
    Then I should see an error message for invalid file type
=======
    Given User launches the application
    And User logs in with valid credentials
    When User navigates to Recruitment module
    And User clicks on "Continue" button for the correct job role
    And User navigates to the "Candidate" upload section
    And User uploads the correct document
    Then the resume should be uploaded successfully
    And candidate should be listed under the correct role

  @Recruitment_Negative
  Scenario: Upload resume with unsupported file format
    Given User launches the application
    And User logs in with valid credentials
    When User navigates to Recruitment module
    And User clicks on "Continue" button for the correct job role
    And User navigates to the "Candidate" upload section
    And User uploads the correct document
    Then the correct error message for invalid file type should be displayed
>>>>>>> a47c1fe2ef3455fd6c1379e7bfde553d708c9201
    And the resume should not be uploaded

  @Recruitment_Delete
  Scenario: Delete candidate from Recruitment module using dynamic resume name
<<<<<<< HEAD
    Given I am logged into the application
    Then I should be on the "Dashboard" page
    When I navigate to Recruitment module
    Then I should be on the "Recruitment" page
    When I click on continue button of ML engineer role
    Then I should be on the "Overview" page
    When I click on "Candidate" tab
    And I switch to table view
    And I click on the three dot menu based on resume name "Prasaanthi"
    Then I click on delete candidate option
    And I capture the confirmation popup text
    And I validate the popup text contains the resume name "Prasaanthi"
    Then I click on delete confirmation button only if validation is successful
=======
    Given User launches the application
    And User logs in with valid credentials
    When User navigates to Recruitment module
    And User clicks on "Continue" button for the correct job role
    And User clicks on "Candidate" tab
    And User switches to table view
    And User deletes the candidate based on the correct resume name
    Then the confirmation popup should contain the correct resume name
    And User confirms the deletion

@Recruitment_Approve_Shortlist
Scenario: Validate Approve Shortlist button behavior and navigation to Interview Management
    Given User launches the application
    And User logs in with valid credentials
    When User navigates to Recruitment module
    And User clicks on "Shortlisting" icon
    And User selects the correct role from the dropdown
    Then "Approve Shortlist" button should be disabled
    When User selects the candidates based on the provided name
    Then "Approve Shortlist" button should be enabled
    When User clicks on "Approve Shortlist" button 
    Then User should be navigated to "Interview Management" page
    And Page should display correctly matched text in Interview Management page

  @Recruitment_GoogleDrive
  Scenario: Connect Google Drive and Verify Candidate Profile
    Given User launches the application
    And User logs in with valid credentials
    When User navigates to Recruitment module
    And User clicks on My Queue icon
    And User searches for and opens a job role
    And User selects the source as "Google Drive" under Configure Data
    And User pastes the Google Drive link
    And User clicks on "Save Configuration" button
    And User navigates to the "Candidates" section
    And User searches for the added profile
    Then the profile should be displayed successfully

  @Recruitment_InterviewSlot
  Scenario: Add interview slot manually and verify date and time
    Given User launches the application
    And User logs in with valid credentials
    When User navigates to Recruitment module
    And User navigates to the "Interviews" section
    And User selects a role from the dropdown dynamically
    Then the "Slot Pool" tab should be enabled
    When User clicks on the "Slot Pool" tab
    And User clicks on "Add Slots" button
    And User enters Start Date, End Date and Interviewer details
    And User clicks on "Create Slots" button
    Then the interview slot should be created successfully

    
  @Recruitment_SyncCalendar
  Scenario: Sync interview slot from calendar and verify date and time
    Given User launches the application
    And User logs in with valid credentials
    When the user navigates to the Interviews page
    And selects a role from the dropdown
    And verifies that the Slot Pool tab is enabled
    And clicks on the Slot Pool tab
    And clicks on "Sync from Calendar"
    And fills all the necessary details
    Then the date and time should be displayed correctly

@Recruitment_Reschedule
  Scenario: Re-schedule interview slot and verify status
    Given User launches the application
    And User logs in with valid credentials
    Then User Navigate to recruitment page
    When the user navigates to the Interviews page
    When the user select Roles from dropdown
    And navigates to the Schedule section
    And selects the Past schedule interviews
    And chooses "Re-schedule" from the Actions menu
    And enters the new Date and Time
    Then the status should be updated successfully

  @Recruitment_SendInvitation
  Scenario: send interview invitation
    Given User launches the application
    And User logs in with valid credentials
    When the user navigates to the Interviews page
    And selects a role from the dropdown
    And click on the invitation tab
    Then Select the candidate and clicking on send button
    And click on Send All button

  @Recruitment_Cancel
  Scenario: Cancel scheduled interview and verify status
    Given User launches the application
    And User logs in with valid credentials
    Then User Navigate to recruitment page
    When the user navigates to the Interviews page
    When the user select Roles from dropdown
    And navigates to the Schedule section
    And selects the Past schedule interviews
    And chooses "Cancel" from the Actions menu
    Then the status should be updated successfully

  @Recruitment_Feedback
  Scenario: Submit feedback and verify
    Given User launches the application
    And User logs in with valid credentials
    Then User Navigate to recruitment page
    When the user navigates to the Interviews page
    When the user select Roles from dropdown
    Then select the feedback section
    And select the submitted option
    When click on review button in actions
    Then validate the status and brightfit score







>>>>>>> a47c1fe2ef3455fd6c1379e7bfde553d708c9201
