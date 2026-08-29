import java.io.IOException;
import java.io.PrintWriter;
import java.util.Date;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;

@WebServlet("/date")
public class DateServlet extends HttpServlet {

    protected void doGet(HttpServletRequest request,
            HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/html");
        PrintWriter out = response.getWriter();

        out.println("<html>");
        out.println("<head><title>Current Date & Time</title></head>");
        out.println("<body style='font-family: Arial, sans-serif; background-color: #f4f6f9; padding: 40px;'>");
        out.println(
                "<div style='background: white; max-width: 600px; margin: 0 auto; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;'>");
        out.println("<h2 style='color: #2c3e50;'>Server Date & Time Servlet</h2>");
        out.println("<hr style='border: 0; border-top: 1px solid #eee; margin: 20px 0;'>");
        out.println("<p style='font-size: 18px; color: #34495e;'>Current Server Time:</p>");
        out.println("<h3 style='color: #e74c3c; font-size: 24px;'>" + new Date().toString() + "</h3>");
        out.println("</div>");
        out.println("</body>");
        out.println("</html>");
    }
}