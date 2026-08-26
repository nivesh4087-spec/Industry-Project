# Responsive Electricity Bill Calculator Application
Built with Java Servlet, JSP, HTML5, CSS3, Bootstrap 5, and jQuery.

## Slab Tariff Rates
- First 50 units: **Rs. 3.50 / unit**
- Next 100 units (51-150): **Rs. 4.00 / unit**
- Next 100 units (151-250): **Rs. 5.20 / unit**
- Above 250 units (> 250): **Rs. 6.50 / unit**

## Project Structure
- `index.html`: Standalone interactive responsive web application with Bootstrap 5, jQuery, Chart.js
- `web/index.jsp`: JSP input form page
- `web/bill_result.jsp`: JSP result page with bill breakdown
- `src/com/electricity/CalculateBillServlet.java`: Java Servlet handling bill logic
- `src/com/electricity/BillBean.java`: Java Data Model
- `web/WEB-INF/web.xml`: Deployment descriptor
- `generate_report_pdf.py`: Python script generating the documentation PDF with screenshots