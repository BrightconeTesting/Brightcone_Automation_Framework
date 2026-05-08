Feature: User Login with OTP
  To ensure secure access to the Brightcone dashboard.

  @login
  Scenario: Login using email and OTP
<<<<<<< HEAD
    Given I open the Brightcone login page
    When I enter my email "munjalaharikrishna123@gmail.com"
    And I click on the Continue button
    Then I fetch the latest 6-digit OTP from my Gmail inbox
    And I enter the 6-digit OTP into separate input fields
    And I click on the Login button
    Then I should be successfully logged in to the dashboard
=======
    Given User launches the application
    And User logs in with valid credentials
    Then User should be successfully logged in to the dashboard

>>>>>>> a47c1fe2ef3455fd6c1379e7bfde553d708c9201
