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
    And I click on the three dot menu based on resume name "Prasaanthi"
    Then I click on delete candidate option
    And I capture the confirmation popup text
    And I validate the popup text contains the resume name "Prasaanthi"
    Then I click on delete confirmation button only if validation is successful
