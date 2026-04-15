@Recruitment
Feature: Resume Management in Recruitment Module
  I want to add candidates and upload resumes for specific job roles,

  @Recruitment_Possitive
  Scenario: Add a resume for ML Engineer role
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
    And the resume should not be uploaded

  @Recruitment_Delete
  Scenario: Delete candidate from Recruitment module using dynamic resume name
    Given I am logged into the application
    Then I should be on the "Dashboard" page
    When I navigate to Recruitment module
    Then I should be on the "Recruitment" page
    When I click on continue button of ML engineer role
    Then I should be on the "Overview" page
    When I click on "Candidate" tab
    And I switch to table view
    And I click on the three dot menu based on resume name "John"
    Then I click on delete candidate option
    And I capture the confirmation popup text
    And I validate the popup text contains the resume name "John"
    Then I click on delete confirmation button only if validation is successful

@Recruitment_Approve_Shortlist
Scenario: Validate Approve Shortlist button behavior and navigation to Interview Management
    Given User is logged into the application
    When User clicks on "Recruitment" side menu
    And User clicks on "Shortlisting" icon
    And User selects "QA Engineer" role from "All Roles" dropdown
    Then "Approve Shortlist" button should be disabled
    When User selects the candidates based on the provided name
    Then "Approve Shortlist" button should be enabled
    When User clicks on "Approve Shortlist" button 
    Then User should be navigated to "Interview Management" page
    And Page should display text "User" in Interview Management page