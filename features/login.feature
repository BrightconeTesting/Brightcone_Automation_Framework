Feature: User Login with OTP
  To ensure secure access to the Brightcone dashboard.

  @login
  Scenario: Login using email and OTP
    Given User launches the application
    And User logs in with valid credentials
    Then User should be successfully logged in to the dashboard

