<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
    <%@ page import="com.electricity.BillBean" %>
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Electricity Bill Calculation Result</title>
            <!-- Bootstrap 5 CSS -->
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <!-- FontAwesome Icons -->
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            <style>
                body {
                    background-color: #0f172a;
                    color: #f8fafc;
                    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                }

                .card-custom {
                    background: #1e293b;
                    border: 1px solid #334155;
                    border-radius: 12px;
                    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
                }

                .invoice-card {
                    background: #ffffff;
                    color: #1e293b;
                    border-radius: 12px;
                }

                .table-custom {
                    color: #f8fafc;
                }

                .table-custom th {
                    background-color: #334155;
                    color: #38bdf8;
                }

                .table-custom td {
                    background-color: #1e293b;
                    border-color: #334155;
                }
            </style>
        </head>

        <body class="py-5">

            <% BillBean bill=(BillBean) request.getAttribute("bill"); if (bill==null) {
                response.sendRedirect("index.jsp"); return; } %>

                <div class="container">
                    <div class="row justify-content-center">
                        <div class="col-lg-9">

                            <!-- Action Bar -->
                            <div class="d-flex align-items-center justify-content-between mb-4">
                                <a href="index.jsp" class="btn btn-outline-light"><i
                                        class="fa-solid fa-arrow-left me-2"></i>Calculate Another Bill</a>
                                <button onclick="window.print()" class="btn btn-success fw-bold"><i
                                        class="fa-solid fa-print me-2"></i>Print Official Invoice</button>
                            </div>

                            <!-- Result Card -->
                            <div class="card card-custom p-4 mb-4">
                                <div
                                    class="d-flex align-items-center justify-content-between mb-3 border-bottom border-secondary pb-3">
                                    <div>
                                        <h3 class="fw-bold text-info mb-1"><i
                                                class="fa-solid fa-file-invoice-dollar me-2"></i>Electricity Bill
                                            Invoice</h3>
                                        <p class="text-secondary mb-0">Consumer: <strong>
                                                <%= bill.getCustomerName() %>
                                            </strong> (<%= bill.getConsumerNo() %>)</p>
                                    </div>
                                    <div class="text-end">
                                        <span class="badge bg-primary px-3 py-2 fs-6">
                                            <%= bill.getConnectionType() %> Category
                                        </span>
                                        <div class="text-secondary small mt-1">Bill Date: <% out.print(new
                                                java.text.SimpleDateFormat("dd MMM yyyy").format(new java.util.Date()));
                                                %>
                                        </div>
                                    </div>
                                </div>

                                <!-- KPI Summary Cards -->
                                <div class="row g-3 mb-4">
                                    <div class="col-md-4">
                                        <div class="p-3 bg-dark border border-secondary rounded text-center">
                                            <div class="text-secondary small text-uppercase">Total Units Consumed</div>
                                            <div class="fs-2 fw-bold text-info">
                                                <%= String.format("%.2f", bill.getTotalUnits()) %> <span
                                                        class="fs-6 text-secondary">kWh</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4">
                                        <div class="p-3 bg-dark border border-secondary rounded text-center">
                                            <div class="text-secondary small text-uppercase">Total Amount Due</div>
                                            <div class="fs-2 fw-bold text-success">₹<%= String.format("%.2f",
                                                    bill.getTotalBillAmount()) %>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-4">
                                        <div class="p-3 bg-dark border border-secondary rounded text-center">
                                            <div class="text-secondary small text-uppercase">Early Payment Amount</div>
                                            <div class="fs-2 fw-bold text-warning">₹<%= String.format("%.2f",
                                                    bill.getEarlyPaymentDiscount()) %>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Slab Breakdown Table -->
                                <h5 class="fw-bold text-light mb-3"><i
                                        class="fa-solid fa-list-check me-2 text-info"></i>Detailed Tariff Slab Breakdown
                                </h5>
                                <div class="table-responsive mb-4">
                                    <table class="table table-custom align-middle">
                                        <thead>
                                            <tr>
                                                <th>Slab Tier Range</th>
                                                <th>Applicable Units</th>
                                                <th>Rate / Unit</th>
                                                <th class="text-end">Cost Component</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <td>Slab 1 (0 to 50 Units)</td>
                                                <td>
                                                    <%= String.format("%.2f", bill.getSlab1Units()) %> kWh
                                                </td>
                                                <td>₹3.50</td>
                                                <td class="text-end">₹<%= String.format("%.2f", bill.getSlab1Cost()) %>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>Slab 2 (51 to 150 Units)</td>
                                                <td>
                                                    <%= String.format("%.2f", bill.getSlab2Units()) %> kWh
                                                </td>
                                                <td>₹4.00</td>
                                                <td class="text-end">₹<%= String.format("%.2f", bill.getSlab2Cost()) %>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>Slab 3 (151 to 250 Units)</td>
                                                <td>
                                                    <%= String.format("%.2f", bill.getSlab3Units()) %> kWh
                                                </td>
                                                <td>₹5.20</td>
                                                <td class="text-end">₹<%= String.format("%.2f", bill.getSlab3Cost()) %>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td>Slab 4 (Above 250 Units)</td>
                                                <td>
                                                    <%= String.format("%.2f", bill.getSlab4Units()) %> kWh
                                                </td>
                                                <td>₹6.50</td>
                                                <td class="text-end">₹<%= String.format("%.2f", bill.getSlab4Cost()) %>
                                                </td>
                                            </tr>
                                            <tr class="fw-bold table-active border-top">
                                                <td colspan="3">Net Energy Charges</td>
                                                <td class="text-end text-info">₹<%= String.format("%.2f",
                                                        bill.getEnergyCharges()) %>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td colspan="3">Fixed Meter / Demand Charge</td>
                                                <td class="text-end">₹<%= String.format("%.2f", bill.getFixedCharge())
                                                        %>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td colspan="3">Electricity Duty Tax (5%)</td>
                                                <td class="text-end">₹<%= String.format("%.2f",
                                                        bill.getElectricityDuty()) %>
                                                </td>
                                            </tr>
                                            <tr class="fw-bold fs-5 text-success border-top border-light">
                                                <td colspan="3">FINAL TOTAL PAYABLE AMOUNT</td>
                                                <td class="text-end">₹<%= String.format("%.2f",
                                                        bill.getTotalBillAmount()) %>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>

                                <!-- Incentive vs Penalty Box -->
                                <div class="row g-3">
                                    <div class="col-md-6">
                                        <div class="p-3 bg-success bg-opacity-10 border border-success rounded">
                                            <h6 class="text-success fw-bold"><i
                                                    class="fa-solid fa-circle-check me-2"></i>Pay On / Before Due Date
                                            </h6>
                                            <div class="fs-5 fw-bold text-light">Payable: ₹<%= String.format("%.2f",
                                                    bill.getEarlyPaymentDiscount()) %>
                                            </div>
                                            <div class="small text-success">Includes 2% Prompt Payment Discount!</div>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="p-3 bg-danger bg-opacity-10 border border-danger rounded">
                                            <h6 class="text-danger fw-bold"><i
                                                    class="fa-solid fa-circle-exclamation me-2"></i>Pay After Due Date
                                            </h6>
                                            <div class="fs-5 fw-bold text-light">Payable: ₹<%= String.format("%.2f",
                                                    bill.getLatePaymentAmount()) %>
                                            </div>
                                            <div class="small text-danger">Includes 5% Late Fee Surcharge!</div>
                                        </div>
                                    </div>
                                </div>

                            </div>
                        </div>
                    </div>
                </div>

                <!-- jQuery & Bootstrap JS -->
                <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        </body>

        </html>