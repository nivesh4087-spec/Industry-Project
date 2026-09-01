<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Square of a Number</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 40px; }
        .container { max-width: 450px; background: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin: 0 auto; }
        h2 { color: #2c3e50; border-bottom: 2px solid #8e44ad; padding-bottom: 10px; font-size: 20px; }
        label { font-weight: bold; display: block; margin-top: 15px; color: #34495e; font-size: 14px; }
        input[type="number"] { width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; font-size: 14px; }
        input[type="submit"] { background-color: #8e44ad; color: white; border: none; padding: 12px 20px; margin-top: 20px; border-radius: 4px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold; }
        input[type="submit"]:hover { background-color: #732d91; }
        .result { margin-top: 20px; padding: 15px; background-color: #f4ecf7; border-left: 5px solid #8e44ad; border-radius: 4px; font-size: 16px; color: #6c3483; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Calculate Square of a Number</h2>
        <form action="q2_square.jsp" method="post">
            <label for="number">Enter a Number:</label>
            <input type="number" step="any" name="number" id="number" required value="<%= request.getParameter("number") != null ? request.getParameter("number") : "" %>">
            
            <input type="submit" value="Calculate Square">
        </form>

        <%
            String numStr = request.getParameter("number");
            if (numStr != null && !numStr.trim().isEmpty()) {
                try {
                    double num = Double.parseDouble(numStr);
                    double square = num * num;
        %>
                    <div class="result">
                        The square of <strong><%= num %></strong> is <strong><%= square %></strong>
                    </div>
        <%
                } catch (NumberFormatException e) {
        %>
                    <div class="result" style="background-color: #fadbd8; border-left-color: #e74c3c; color: #c0392b;">
                        Invalid input! Please enter a valid number.
                    </div>
        <%
                }
            }
        %>
    </div>
</body>
</html>
