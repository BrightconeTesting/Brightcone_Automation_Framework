@uploaded
Feature: Document Upload and Status Validation

  @upload
  Scenario: Upload document and verify its status
    Given User launches the application
    And User logs in with valid credentials
    When User navigates to Documents page
    And User selects the correct category
    And User uploads a document
    And User clicks the "Upload" button
    Then a popup with correctly matched text should appear

