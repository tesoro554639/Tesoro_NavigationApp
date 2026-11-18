# ROOM ACT 7: INTEGRATED FLUTTER STUDENT APPLICATION

**Topic:** Demo Authentication, StatefulWidget, and Bottom Navigation  
**Student Name:** Luis James Tesoro  
**Student ID:** 554639  
**Course & Section:** BSIT — 2nd Year - 4745 (CCE106L)  
**Date:** November 18, 2026  
**Repository:** [https://github.com/tesoro554639/ROOM-ACT-7-INTEGRATED-FLUTTER-STUDENT-APPLICATION](https://github.com/tesoro554639/ROOM-ACT-7-INTEGRATED-FLUTTER-STUDENT-APPLICATION)

---

## Overview

This Flutter application integrates previous laboratory activities into a unified, modular student platform:
- **Authentication (`DemoAuth`):** Handles in-memory session login, registration with validation, and logout. Supports default `admin / admin123` credentials and dynamic user registration.
- **Dashboard (`DashboardPage`):** Greets the authenticated user with a personalized message (`Welcome, $username!`) and provides an overview of application features.
- **Calculator (`CalculatorScreen`):** Full arithmetic operations (+, -, ×, ÷), clear button, input validation, and zero-division protection.
- **Social Media Feed (`SocialMediaPage`):** Interactive feed featuring post creation with caption and image URL validation, like/unlike toggling, dynamic commenting, and state preservation via `ObjectKey(post)`.
- **Student Profile (`ProfilePage`):** Displays student details, active logged-in user, and an integrated Logout workflow that clears session state and resets the navigation stack.
- **State Preservation (`MainScreen`):** Manages a bottom `NavigationBar` with `IndexedStack` to ensure calculation inputs and social feed states remain completely intact across tab switches.

---

## Navigation Destinations

| Index | Destination | Icon | Description |
| :---: | :--- | :--- | :--- |
| **0** | **Dashboard** | `Icons.dashboard` | Personalized welcome message and overview |
| **1** | **Calculator** | `Icons.calculate` | Working arithmetic calculator |
| **2** | **Social** | `Icons.people` | Feed with Create Post, Like, and Comment |
| **3** | **Profile** | `Icons.person` | Student info, active username, and Logout |

---

## Step 11: Application Testing Table (14 Scenarios)

| No. | Test Case / Action | Expected Result | Pass/Fail |
| :-: | :--- | :--- | :-: |
| **1** | Open the application. | Login appears first. | **Pass** |
| **2** | Submit empty login fields. | Validation messages appear. | **Pass** |
| **3** | Enter incorrect credentials. | Login is rejected. | **Pass** |
| **4** | Enter admin / admin123. | Dashboard opens. | **Pass** |
| **5** | Read the dashboard greeting. | Displays `Welcome, admin!` | **Pass** |
| **6** | Open Calculator and calculate 10 + 5. | Displays `15.0`. | **Pass** |
| **7** | Switch tabs and return to Calculator. | Inputs and result remain. | **Pass** |
| **8** | Create a social post. | Post displays the logged-in username. | **Pass** |
| **9** | Like a post and add a comment. | Both interactions update correctly. | **Pass** |
| **10** | Switch tabs and return to Social. | Posts, likes, and comments remain. | **Pass** |
| **11** | Open Profile. | Student information and username appear. | **Pass** |
| **12** | Tap Logout. | Login appears; Back does not reopen MainScreen. | **Pass** |
| **13** | Register a valid account and log in. | Dashboard displays the registered username. | **Pass** |
| **14** | Create a post using the registered account. | Post displays the registered username. | **Pass** |

---

## Guide Questions & Answers

1. **How does DemoAuth connect Login to Dashboard, Social, and Profile?**  
   `DemoAuth` acts as a shared in-memory authentication repository that records `currentUsername` upon successful credential validation in `LoginScreen`. When `MainScreen` initializes, it retrieves this recorded username and supplies it directly to the constructors of `DashboardPage`, `SocialMediaPage`, and `ProfilePage`. This ensures all pages display consistent personalized greetings, author tags, and account details.

2. **Why must the order of pages match the bottom navigation destinations?**  
   In `MainScreen`, the `NavigationBar` sends its destination index (0 to 3) to the `IndexedStack`. Because `IndexedStack` displays the child widget situated at that exact index position, the order of widgets in the `pages` list must mirror the navigation bar destinations (Dashboard: 0, Calculator: 1, Social: 2, Profile: 3). Any mismatch would cause tapping an item to open a different screen.

3. **Why is IndexedStack useful for the Calculator and Social pages?**  
   Standard navigation or conditional rendering rebuilds and disposes page state whenever a user switches views. `IndexedStack` keeps all child widgets mounted simultaneously in the widget tree, hiding inactive pages offstage without disposing them. This preserves calculator inputs, calculated results, custom social posts, liked states, and user comments across tab switches.

4. **Why should Logout clear the current username and remove previous routes?**  
   Setting `DemoAuth.currentUsername = null` resets the authentication session so subsequent requests cannot access previous user data. Using `Navigator.pushAndRemoveUntil(..., (route) => false)` clears the entire navigation history stack, preventing users from bypassing authentication by pressing the device Back button.

5. **Which information is lost when this demo application restarts?**  
   Because this demo stores runtime state entirely in volatile RAM without persistent storage (such as SQLite or SharedPreferences), all registered user accounts, custom social posts, likes, comments, and calculator history are completely lost on restart. Only hardcoded defaults, such as the static admin credentials (`admin / admin123`) and initial sample posts, remain.

---

## Running the Application

```bash
# Get dependencies
flutter pub get

# Run test suite
flutter test

# Run application
flutter run
```
