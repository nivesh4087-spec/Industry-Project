<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>User Authentication System</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 40px; }
        .container { max-width: 450px; background: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin: 0 auto; }
        h2 { color: #2c3e50; border-bottom: 2px solid #2980b9; padding-bottom: 10px; font-size: 20px; }
        label { font-weight: bold; display: block; margin-top: 15px; color: #34495e; font-size: 14px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; font-size: 14px; }
        input[type="submit"] { background-color: #2980b9; color: white; border: none; padding: 12px 20px; margin-top: 20px; border-radius: 4px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold; }
        input[type="submit"]:hover { background-color: #1b4f72; }
        .status-success { margin-top: 20px; padding: 15px; background-color: #d4efdf; border-left: 5px solid #27ae60; color: #1e8449; border-radius: 4px; font-size: 15px; }
        .status-error { margin-top: 20px; padding: 15px; background-color: #fadbd8; border-left: 5px solid #e74c3c; color: #78281f; border-radius: 4px; font-size: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>User Login Portal</h2>
        <form action="q5_auth.jsp" method="post">
            <label for="username">Username:</label>
            <input type="text" name="username" id="username" placeholder="Enter username" required value="<%= request.getParameter("username") != null ? request.getParameter("username") : "" %>">
            
            <label for="password">Password:</label>
            <input type="password" name="password" id="password" placeholder="Enter password" required>
            
            <input type="submit" value="Login">
        </form>

        <%
            String uname = request.getParameter("username");
            String pass = request.getParameter("password");

            if (uname != null && pass != null) {
                // Hardcoded credentials check for demonstration
                String validUsername = "admin";
                String validPassword = "password123";

                if (uname.equals(validUsername) && pass.equals(validPassword)) {
        %>
                    <div class="status-success">
                        <strong>Login Successful!</strong><br>
                        Welcome back, <strong><%= uname %></strong>. Access granted to the system portal.
                    </div>
        <%
                } else {
        %>
                    <div class="status-error">
                        <strong>Authentication Failed!</strong><br>
                        Invalid username or password. Please try again.
                    </div>
        <%
                }
            }
        %>
    </div>
</body>
</html>
