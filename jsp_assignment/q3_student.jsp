<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Student Registration & Details</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 40px; }
        .container { max-width: 500px; background: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin: 0 auto; }
        h2 { color: #2c3e50; border-bottom: 2px solid #16a085; padding-bottom: 10px; font-size: 20px; }
        label { font-weight: bold; display: block; margin-top: 15px; color: #34495e; font-size: 14px; }
        input[type="text"], input[type="number"], select { width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; font-size: 14px; }
        input[type="submit"] { background-color: #16a085; color: white; border: none; padding: 12px 20px; margin-top: 20px; border-radius: 4px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold; }
        input[type="submit"]:hover { background-color: #117864; }
        .details-card { margin-top: 25px; padding: 20px; background-color: #e8f8f5; border: 1px solid #a3e4d7; border-radius: 6px; }
        .details-card h3 { margin-top: 0; color: #117864; border-bottom: 1px solid #a3e4d7; padding-bottom: 8px; font-size: 18px; }
        .detail-row { margin: 10px 0; font-size: 15px; color: #2c3e50; }
        .detail-label { font-weight: bold; color: #16a085; width: 120px; display: inline-block; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Student Information Form</h2>
        <form action="q3_student.jsp" method="post">
            <label for="studentName">Student Name:</label>
            <input type="text" name="studentName" id="studentName" placeholder="e.g. Nivesh Jain" required value="<%= request.getParameter("studentName") != null ? request.getParameter("studentName") : "" %>">
            
            <label for="age">Age:</label>
            <input type="number" name="age" id="age" min="1" max="100" placeholder="e.g. 21" required value="<%= request.getParameter("age") != null ? request.getParameter("age") : "" %>">
            
            <label for="department">Department:</label>
            <select name="department" id="department" required>
                <option value="">-- Select Department --</option>
                <option value="Computer Engineering" <%= "Computer Engineering".equals(request.getParameter("department")) ? "selected" : "" %>>Computer Engineering</option>
                <option value="Information Technology" <%= "Information Technology".equals(request.getParameter("department")) ? "selected" : "" %>>Information Technology</option>
                <option value="Artificial Intelligence & Data Science" <%= "Artificial Intelligence & Data Science".equals(request.getParameter("department")) ? "selected" : "" %>>Artificial Intelligence & Data Science</option>
                <option value="Electronics & Telecommunication" <%= "Electronics & Telecommunication".equals(request.getParameter("department")) ? "selected" : "" %>>Electronics & Telecommunication</option>
                <option value="Mechanical Engineering" <%= "Mechanical Engineering".equals(request.getParameter("department")) ? "selected" : "" %>>Mechanical Engineering</option>
            </select>
            
            <input type="submit" value="Submit Student Details">
        </form>

        <%
            String name = request.getParameter("studentName");
            String ageStr = request.getParameter("age");
            String dept = request.getParameter("department");

            if (name != null && ageStr != null && dept != null && !name.trim().isEmpty()) {
        %>
                <div class="details-card">
                    <h3>Submitted Student Details</h3>
                    <div class="detail-row"><span class="detail-label">Name:</span> <%= name %></div>
                    <div class="detail-row"><span class="detail-label">Age:</span> <%= ageStr %> years old</div>
                    <div class="detail-row"><span class="detail-label">Department:</span> <%= dept %></div>
                </div>
        <%
            }
        %>
    </div>
</body>
</html>
