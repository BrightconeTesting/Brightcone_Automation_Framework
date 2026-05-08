@Documents
Feature: Document Upload and Status Validation

  @upload
  Scenario: Upload document and verify its status
    Given User launches the application
    And User logs in with valid credentials
<<<<<<< HEAD
    Then User should be on the "Dashboard" page
    When User navigates to Documents page
    Then User should be on the "Documents" page
    When User uploads a document
    And User selects the "Admin", "Engineering" and "Support" categories
    And User clicks the "Upload" button
    Then a popup with text "Sensitive information detected. This has been flagged for review." should appear
    And Uploaded document should be visible in My Uploads
    And User should capture the document name
=======
    When User navigates to Documents page
    And User selects the correct category
    And User uploads a document
    And User clicks the "Upload" button
    Then a popup with correctly matched text should appear
  
>>>>>>> a47c1fe2ef3455fd6c1379e7bfde553d708c9201
