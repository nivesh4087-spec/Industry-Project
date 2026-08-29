import java.io.IOException;
import java.io.PrintWriter;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;

@WebServlet("/hello")
public class HelloServlet extends HttpServlet {

    protected void doGet(HttpServletRequest request,
            HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/html");
        PrintWriter out = response.getWriter();

        out.println("<html>");
        out.println("<head><title>Hello Servlet</title></head>");
        out.println("<body style='font-family: Arial, sans-serif; background-color: #f4f6f9; padding: 40px;'>");
        out.println(
                "<div style='background: white; max-width: 600px; margin: 0 auto; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;'>");
        out.println("<h1 style='color: #2c3e50;'>Hello World</h1>");
        out.println("<p style='color: #7f8c8d; font-size: 16px;'>Welcome to Basic Java Servlet Demonstration</p>");
        out.println("<hr style='border: 0; border-top: 1px solid #eee; margin: 20px 0;'>");
        out.println("<p style='color: #27ae60; font-weight: bold;'>Status: Servlet Executed Successfully!</p>");
        out.println("</div>");
        out.println("</body>");
        out.println("</html>");
    }
}