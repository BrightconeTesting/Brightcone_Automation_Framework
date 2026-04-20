@Recruitment
Feature: Resume Management in Recruitment Module
  I want to add candidates and upload resumes for specific job roles,

  @Recruitment_Possitive
  Scenario: Add a resume for ML Engineer role
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
    And the resume should not be uploaded

  @Recruitment_Delete
  Scenario: Delete candidate from Recruitment module using dynamic resume name
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