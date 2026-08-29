import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.file.Files;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

public class SimpleServletContainer {

    public static void main(String[] args) throws Exception {
        int port = 8080;
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);

        System.out.println("Servlet Demo Container running on http://localhost:" + port + "/ServletDemo/");

        server.createContext("/ServletDemo/hello", new HttpHandler() {
            @Override
            public void handle(HttpExchange exchange) throws IOException {
                String response = "<html>" +
                        "<head><title>Hello Servlet</title></head>" +
                        "<body style='font-family: Arial, sans-serif; background-color: #f4f6f9; padding: 40px;'>" +
                        "<div style='background: white; max-width: 600px; margin: 0 auto; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;'>"
                        +
                        "<h1 style='color: #2c3e50;'>Hello World</h1>" +
                        "<p style='color: #7f8c8d; font-size: 16px;'>Welcome to Basic Java Servlet Demonstration</p>" +
                        "<hr style='border: 0; border-top: 1px solid #eee; margin: 20px 0;'>" +
                        "<p style='color: #27ae60; font-weight: bold;'>Status: Servlet Executed Successfully!</p>" +
                        "</div>" +
                        "</body>" +
                        "</html>";
                exchange.getResponseHeaders().set("Content-Type", "text/html; charset=UTF-8");
                byte[] bytes = response.getBytes("UTF-8");
                exchange.sendResponseHeaders(200, bytes.length);
                OutputStream os = exchange.getResponseBody();
                os.write(bytes);
                os.close();
            }
        });

        server.createContext("/ServletDemo/date", new HttpHandler() {
            @Override
            public void handle(HttpExchange exchange) throws IOException {
                String response = "<html>" +
                        "<head><title>Current Date & Time</title></head>" +
                        "<body style='font-family: Arial, sans-serif; background-color: #f4f6f9; padding: 40px;'>" +
                        "<div style='background: white; max-width: 600px; margin: 0 auto; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;'>"
                        +
                        "<h2 style='color: #2c3e50;'>Server Date & Time Servlet</h2>" +
                        "<hr style='border: 0; border-top: 1px solid #eee; margin: 20px 0;'>" +
                        "<p style='font-size: 18px; color: #34495e;'>Current Server Time:</p>" +
                        "<h3 style='color: #e74c3c; font-size: 24px;'>" + new Date().toString() + "</h3>" +
                        "</div>" +
                        "</body>" +
                        "</html>";
                exchange.getResponseHeaders().set("Content-Type", "text/html; charset=UTF-8");
                byte[] bytes = response.getBytes("UTF-8");
                exchange.sendResponseHeaders(200, bytes.length);
                OutputStream os = exchange.getResponseBody();
                os.write(bytes);
                os.close();
            }
        });

        server.createContext("/ServletDemo/welcome", new HttpHandler() {
            @Override
            public void handle(HttpExchange exchange) throws IOException {
                String query = exchange.getRequestURI().getQuery();
                Map<String, String> params = parseQuery(query);

                String username = params.get("username");
                if (username == null || username.trim().isEmpty()) {
                    username = params.get("user");
                }
                if (username == null || username.trim().isEmpty()) {
                    username = "Guest";
                }

                String response = "<html>" +
                        "<head><title>Welcome Servlet</title></head>" +
                        "<body style='font-family: Arial, sans-serif; background-color: #f4f6f9; padding: 40px;'>" +
                        "<div style='background: white; max-width: 600px; margin: 0 auto; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;'>"
                        +
                        "<h1 style='color: #2c3e50;'>Welcome " + username + "</h1>" +
                        "<p style='color: #7f8c8d; font-size: 16px;'>Form data successfully processed by HttpServlet Request parameters.</p>"
                        +
                        "<hr style='border: 0; border-top: 1px solid #eee; margin: 20px 0;'>" +
                        "<a href='index.html' style='display: inline-block; padding: 10px 20px; background-color: #3498db; color: white; text-decoration: none; border-radius: 4px;'>Back to Form</a>"
                        +
                        "</div>" +
                        "</body>" +
                        "</html>";
                exchange.getResponseHeaders().set("Content-Type", "text/html; charset=UTF-8");
                byte[] bytes = response.getBytes("UTF-8");
                exchange.sendResponseHeaders(200, bytes.length);
                OutputStream os = exchange.getResponseBody();
                os.write(bytes);
                os.close();
            }
        });

        server.createContext("/ServletDemo/", new HttpHandler() {
            @Override
            public void handle(HttpExchange exchange) throws IOException {
                File file = new File("ServletDemo/WebContent/index.html");
                if (!file.exists()) {
                    file = new File("WebContent/index.html");
                }
                if (file.exists()) {
                    byte[] bytes = Files.readAllBytes(file.toPath());
                    exchange.getResponseHeaders().set("Content-Type", "text/html; charset=UTF-8");
                    exchange.sendResponseHeaders(200, bytes.length);
                    OutputStream os = exchange.getResponseBody();
                    os.write(bytes);
                    os.close();
                } else {
                    String notFound = "<h1>404 Not Found</h1>";
                    exchange.sendResponseHeaders(404, notFound.length());
                    OutputStream os = exchange.getResponseBody();
                    os.write(notFound.getBytes());
                    os.close();
                }
            }
        });

        server.setExecutor(null);
        server.start();
    }

    private static Map<String, String> parseQuery(String query) {
        Map<String, String> result = new HashMap<>();
        if (query == null || query.isEmpty())
            return result;
        for (String param : query.split("&")) {
            String[] entry = param.split("=");
            if (entry.length > 1) {
                result.put(entry[0], entry[1]);
            } else if (entry.length == 1) {
                result.put(entry[0], "");
            }
        }
        return result;
    }
}