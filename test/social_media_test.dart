import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:tesoro_navigation_app/demo_auth.dart';
import 'package:tesoro_navigation_app/main.dart';
import 'package:tesoro_navigation_app/main_screen.dart';
import 'package:tesoro_navigation_app/login_screen.dart';
import 'package:tesoro_navigation_app/register_screen.dart';

void main() {
  setUp(() {
    DemoAuth.registeredUsername = null;
    DemoAuth.registeredPassword = null;
    DemoAuth.currentUsername = null;
  });

  testWidgets('Test 1: Open the application - Login appears first', (tester) async {
    await tester.pumpWidget(const StudentApp());
    await tester.pumpAndSettle();

    expect(find.byType(LoginScreen), findsOneWidget);
    expect(find.text('Welcome Back!'), findsOneWidget);
    expect(find.text('Login'), findsWidgets);
  });

  testWidgets('Test 2: Submit empty login fields - Validation messages appear', (tester) async {
    await tester.pumpWidget(const StudentApp());
    await tester.pumpAndSettle();

    await tester.tap(find.widgetWithText(ElevatedButton, 'Login'));
    await tester.pumpAndSettle();

    expect(find.text('Enter your username.'), findsOneWidget);
    expect(find.text('Enter your password.'), findsOneWidget);
  });

  testWidgets('Test 3: Enter incorrect credentials - Login is rejected', (tester) async {
    await tester.pumpWidget(const StudentApp());
    await tester.pumpAndSettle();

    final textFields = find.byType(TextFormField);
    await tester.enterText(textFields.at(0), 'wronguser');
    await tester.enterText(textFields.at(1), 'wrongpass');
    await tester.tap(find.widgetWithText(ElevatedButton, 'Login'));
    await tester.pumpAndSettle();

    expect(find.text('Invalid username or password.'), findsOneWidget);
    expect(find.byType(MainScreen), findsNothing);
  });

  testWidgets('Test 4 & 5: Enter admin / admin123 - Dashboard opens and displays Welcome, admin!', (tester) async {
    await tester.pumpWidget(const StudentApp());
    await tester.pumpAndSettle();

    final textFields = find.byType(TextFormField);
    await tester.enterText(textFields.at(0), 'admin');
    await tester.enterText(textFields.at(1), 'admin123');
    await tester.tap(find.widgetWithText(ElevatedButton, 'Login'));
    await tester.pumpAndSettle();

    expect(find.byType(MainScreen), findsOneWidget);
    expect(find.text('Welcome, admin!'), findsOneWidget);
    expect(find.text('Dashboard'), findsWidgets);
  });

  testWidgets('Test 6 & 7: Calculator 10 + 5 displays 15.0 and switching tabs preserves inputs and result', (tester) async {
    DemoAuth.login('admin', 'admin123');
    await tester.pumpWidget(const MaterialApp(home: MainScreen()));
    await tester.pumpAndSettle();

    // Switch to Calculator tab (index 1)
    await tester.tap(find.byType(NavigationDestination).at(1));
    await tester.pumpAndSettle();

    // Input 10 and 5, tap +
    final inputs = find.byType(TextField);
    await tester.enterText(inputs.at(0), '10');
    await tester.enterText(inputs.at(1), '5');
    await tester.tap(find.widgetWithText(ElevatedButton, '+'));
    await tester.pumpAndSettle();

    expect(find.text('15.0'), findsOneWidget);

    // Switch to Dashboard tab (index 0)
    await tester.tap(find.byType(NavigationDestination).at(0));
    await tester.pumpAndSettle();
    expect(find.text('Welcome, admin!'), findsOneWidget);

    // Switch back to Calculator tab (index 1)
    await tester.tap(find.byType(NavigationDestination).at(1));
    await tester.pumpAndSettle();

    // Verify inputs and result remain
    expect(find.text('15.0'), findsOneWidget);
    expect(find.text('10'), findsOneWidget);
    expect(find.text('5'), findsOneWidget);
  });

  testWidgets('Test 8, 9 & 10: Create social post, like, comment, and switch tabs preservation', (tester) async {
    tester.view.physicalSize = const Size(800, 1600);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(() {
      tester.view.resetPhysicalSize();
      tester.view.resetDevicePixelRatio();
    });

    DemoAuth.login('admin', 'admin123');
    await tester.pumpWidget(const MaterialApp(home: MainScreen()));
    await tester.pumpAndSettle();

    // Switch to Social tab (index 2)
    await tester.tap(find.byType(NavigationDestination).at(2));
    await tester.pumpAndSettle();

    // Create a social post
    await tester.tap(find.byType(FloatingActionButton));
    await tester.pumpAndSettle();

    await tester.enterText(find.widgetWithText(TextField, 'Caption'), 'Admin test post!');
    await tester.enterText(find.widgetWithText(TextField, 'Image URL'), 'https://picsum.photos/id/20/600/400');
    await tester.tap(find.text('Submit Post'));
    await tester.pumpAndSettle();

    // Post displays logged-in username
    expect(find.text('Admin test post!'), findsOneWidget);
    expect(find.text('admin'), findsWidgets);

    // Like the post
    final likeButton = find.widgetWithText(TextButton, 'Like').first;
    await tester.tap(likeButton);
    await tester.pumpAndSettle();
    expect(find.text('Liked'), findsOneWidget);

    // Add a comment
    final commentField = find.byType(TextField).first;
    await tester.enterText(commentField, 'First admin comment');
    await tester.tap(find.byIcon(Icons.send).first);
    await tester.pumpAndSettle();

    expect(find.text('1 Comments'), findsOneWidget);
    expect(find.text('First admin comment'), findsOneWidget);

    // Switch to Dashboard (index 0)
    await tester.tap(find.byIcon(Icons.dashboard_outlined));
    await tester.pumpAndSettle();
    expect(find.text('Welcome, admin!'), findsOneWidget);

    // Switch back to Social (index 2)
    await tester.tap(find.byIcon(Icons.people_outlined));
    await tester.pumpAndSettle();

    // Verify posts, likes, and comments remain
    expect(find.text('Admin test post!'), findsOneWidget);
    expect(find.text('Liked'), findsOneWidget);
    expect(find.text('First admin comment'), findsOneWidget);
  });

  testWidgets('Test 11 & 12: Open Profile displays student info and username, and Logout redirects to Login', (tester) async {
    tester.view.physicalSize = const Size(800, 1600);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(() {
      tester.view.resetPhysicalSize();
      tester.view.resetDevicePixelRatio();
    });

    DemoAuth.login('admin', 'admin123');
    await tester.pumpWidget(const MaterialApp(home: MainScreen()));
    await tester.pumpAndSettle();

    // Switch to Profile (index 3)
    await tester.tap(find.byType(NavigationDestination).at(3));
    await tester.pumpAndSettle();

    // Verify student details and username appear
    expect(find.text('Luis James Tesoro'), findsOneWidget);
    expect(find.text('Logged in as: admin'), findsOneWidget);
    expect(find.text('Student ID'), findsOneWidget);
    expect(find.text('554639'), findsOneWidget);

    // Tap Logout button
    await tester.tap(find.widgetWithText(ElevatedButton, 'Logout'));
    await tester.pumpAndSettle();

    // Verify Login appears and DemoAuth.currentUsername is cleared
    expect(find.byType(LoginScreen), findsOneWidget);
    expect(DemoAuth.currentUsername, isNull);
  });

  testWidgets('Test 13 & 14: Register a valid account and log in - Dashboard and Posts display registered username', (tester) async {
    tester.view.physicalSize = const Size(800, 1600);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(() {
      tester.view.resetPhysicalSize();
      tester.view.resetDevicePixelRatio();
    });

    await tester.pumpWidget(const StudentApp());
    await tester.pumpAndSettle();

    // Navigate to Register
    await tester.tap(find.text('Don\'t have an account? Register'));
    await tester.pumpAndSettle();
    expect(find.byType(RegisterScreen), findsOneWidget);

    // Register user 'maria_santos'
    final regInputs = find.byType(TextFormField);
    await tester.enterText(regInputs.at(0), 'maria_santos');
    await tester.enterText(regInputs.at(1), 'password123');
    await tester.enterText(regInputs.at(2), 'password123');
    await tester.tap(find.widgetWithText(ElevatedButton, 'Register'));
    await tester.pumpAndSettle();

    // Returned to LoginScreen
    expect(find.byType(LoginScreen), findsOneWidget);

    // Login with registered credentials
    final loginInputs = find.byType(TextFormField);
    await tester.enterText(loginInputs.at(0), 'maria_santos');
    await tester.enterText(loginInputs.at(1), 'password123');
    await tester.tap(find.widgetWithText(ElevatedButton, 'Login'));
    await tester.pumpAndSettle();

    // 13. Dashboard displays registered username
    expect(find.byType(MainScreen), findsOneWidget);
    expect(find.text('Welcome, maria_santos!'), findsOneWidget);

    // Dismiss any residual SnackBar from registration
    ScaffoldMessenger.of(tester.element(find.byType(MainScreen))).clearSnackBars();
    await tester.pumpAndSettle();

    // Switch to Social tab (index 2)
    await tester.tap(find.byType(NavigationDestination).at(2));
    await tester.pumpAndSettle();

    // Create a post
    await tester.tap(find.byType(FloatingActionButton));
    await tester.pumpAndSettle();

    await tester.enterText(find.widgetWithText(TextField, 'Caption'), 'Post by Maria!');
    await tester.enterText(find.widgetWithText(TextField, 'Image URL'), 'https://picsum.photos/id/40/600/400');
    await tester.tap(find.text('Submit Post'));
    await tester.pumpAndSettle();

    // 14. Post displays registered username
    expect(find.text('Post by Maria!'), findsOneWidget);
    expect(find.text('maria_santos'), findsOneWidget);
  });
}
