<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Personalized Welcome Message</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 40px; }
        .container { max-width: 450px; background: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin: 0 auto; }
        h2 { color: #2c3e50; border-bottom: 2px solid #e67e22; padding-bottom: 10px; font-size: 20px; }
        label { font-weight: bold; display: block; margin-top: 15px; color: #34495e; font-size: 14px; }
        input[type="text"] { width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; font-size: 14px; }
        input[type="submit"] { background-color: #e67e22; color: white; border: none; padding: 12px 20px; margin-top: 20px; border-radius: 4px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold; }
        input[type="submit"]:hover { background-color: #d35400; }
        .welcome-card { margin-top: 20px; padding: 20px; background-color: #fef5e7; border-left: 5px solid #e67e22; border-radius: 4px; }
        .welcome-card h3 { margin: 0 0 10px 0; color: #d35400; font-size: 18px; }
        .welcome-card p { margin: 0; color: #7f8c8d; font-size: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Welcome Portal</h2>
        <form action="q4_welcome.jsp" method="post">
            <label for="userName">Enter Your Name:</label>
            <input type="text" name="userName" id="userName" placeholder="e.g. Nivesh Jain" required value="<%= request.getParameter("userName") != null ? request.getParameter("userName") : "" %>">
            
            <input type="submit" value="Get Welcome Message">
        </form>

        <%
            String userName = request.getParameter("userName");
            if (userName != null && !userName.trim().isEmpty()) {
        %>
                <div class="welcome-card">
                    <h3>Hello, <%= userName %>! 👋</h3>
                    <p>Welcome to our Java Server Pages (JSP) Application. We are delighted to have you here!</p>
                </div>
        <%
            }
        %>
    </div>
</body>
</html>
