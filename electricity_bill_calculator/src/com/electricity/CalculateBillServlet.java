package com.electricity;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/CalculateBillServlet")
public class CalculateBillServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        try {
            String customerName = request.getParameter("customerName");
            String consumerNo = request.getParameter("consumerNo");
            String connectionType = request.getParameter("connectionType");
            double units = Double.parseDouble(request.getParameter("units"));

            BillBean bill = new BillBean();
            bill.setCustomerName(customerName != null ? customerName : "Valued Customer");
            bill.setConsumerNo(consumerNo != null ? consumerNo : "CONSUMER-1001");
            bill.setConnectionType(connectionType != null ? connectionType : "Domestic");
            bill.setTotalUnits(units);

            // Tiered Tariff Rate Calculation
            // Slab 1: First 50 units @ Rs 3.50
            // Slab 2: Next 100 units @ Rs 4.00
            // Slab 3: Next 100 units @ Rs 5.20
            // Slab 4: Above 250 units @ Rs 6.50

            double slab1Units = 0, slab2Units = 0, slab3Units = 0, slab4Units = 0;
            double slab1Cost = 0, slab2Cost = 0, slab3Cost = 0, slab4Cost = 0;

            double remainingUnits = units;

            if (remainingUnits > 0) {
                slab1Units = Math.min(remainingUnits, 50);
                slab1Cost = slab1Units * 3.50;
                remainingUnits -= slab1Units;
            }

            if (remainingUnits > 0) {
                slab2Units = Math.min(remainingUnits, 100);
                slab2Cost = slab2Units * 4.00;
                remainingUnits -= slab2Units;
            }

            if (remainingUnits > 0) {
                slab3Units = Math.min(remainingUnits, 100);
                slab3Cost = slab3Units * 5.20;
                remainingUnits -= slab3Units;
            }

            if (remainingUnits > 0) {
                slab4Units = remainingUnits;
                slab4Cost = slab4Units * 6.50;
            }

            double energyCharges = slab1Cost + slab2Cost + slab3Cost + slab4Cost;

            // Adjust multiplier for Commercial / Industrial
            if ("Commercial".equalsIgnoreCase(connectionType)) {
                energyCharges *= 1.25; // 25% commercial tariff multiplier
            } else if ("Industrial".equalsIgnoreCase(connectionType)) {
                energyCharges *= 1.50; // 50% industrial tariff multiplier
            }

            double fixedCharge = 50.0; // Fixed meter charge
            double electricityDuty = energyCharges * 0.05; // 5% electricity duty tax
            double totalBillAmount = energyCharges + fixedCharge + electricityDuty;
            double earlyPaymentDiscount = totalBillAmount * 0.98; // 2% discount
            double latePaymentAmount = totalBillAmount * 1.05; // 5% late fee penalty

            // Store inside Bean
            bill.setSlab1Units(slab1Units);
            bill.setSlab1Cost(slab1Cost);
            bill.setSlab2Units(slab2Units);
            bill.setSlab2Cost(slab2Cost);
            bill.setSlab3Units(slab3Units);
            bill.setSlab3Cost(slab3Cost);
            bill.setSlab4Units(slab4Units);
            bill.setSlab4Cost(slab4Cost);
            bill.setEnergyCharges(energyCharges);
            bill.setFixedCharge(fixedCharge);
            bill.setElectricityDuty(electricityDuty);
            bill.setTotalBillAmount(totalBillAmount);
            bill.setEarlyPaymentDiscount(earlyPaymentDiscount);
            bill.setLatePaymentAmount(latePaymentAmount);

            // Forward to JSP
            request.setAttribute("bill", bill);
            request.getRequestDispatcher("bill_result.jsp").forward(request, response);

        } catch (Exception e) {
            request.setAttribute("errorMessage", "Invalid Input! Please enter valid numeric values for units.");
            request.getRequestDispatcher("index.jsp").forward(request, response);
        }
    }

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.sendRedirect("index.jsp");
    }
}