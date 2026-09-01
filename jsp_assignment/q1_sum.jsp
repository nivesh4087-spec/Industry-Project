<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Sum of Two Numbers</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 40px; }
        .container { max-width: 450px; background: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin: 0 auto; }
        h2 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; font-size: 20px; }
        label { font-weight: bold; display: block; margin-top: 15px; color: #34495e; font-size: 14px; }
        input[type="number"] { width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; font-size: 14px; }
        input[type="submit"] { background-color: #3498db; color: white; border: none; padding: 12px 20px; margin-top: 20px; border-radius: 4px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold; }
        input[type="submit"]:hover { background-color: #2980b9; }
        .result { margin-top: 20px; padding: 15px; background-color: #e8f8f5; border-left: 5px solid #2ecc71; border-radius: 4px; font-size: 16px; color: #27ae60; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Calculate Sum of Two Numbers</h2>
        <form action="q1_sum.jsp" method="post">
            <label for="num1">First Number:</label>
            <input type="number" step="any" name="num1" id="num1" required value="<%= request.getParameter("num1") != null ? request.getParameter("num1") : "" %>">
            
            <label for="num2">Second Number:</label>
            <input type="number" step="any" name="num2" id="num2" required value="<%= request.getParameter("num2") != null ? request.getParameter("num2") : "" %>">
            
            <input type="submit" value="Calculate Sum">
        </form>

        <%
            String n1Str = request.getParameter("num1");
            String n2Str = request.getParameter("num2");
            if (n1Str != null && n2Str != null && !n1Str.trim().isEmpty() && !n2Str.trim().isEmpty()) {
                try {
                    double num1 = Double.parseDouble(n1Str);
                    double num2 = Double.parseDouble(n2Str);
                    double sum = num1 + num2;
        %>
                    <div class="result">
                        <strong>Result:</strong> <%= num1 %> + <%= num2 %> = <strong><%= sum %></strong>
                    </div>
        <%
                } catch (NumberFormatException e) {
        %>
                    <div class="result" style="background-color: #fadbd8; border-left-color: #e74c3c; color: #c0392b;">
                        Invalid input! Please enter valid numeric values.
                    </div>
        <%
                }
            }
        %>
    </div>
</body>
</html>
