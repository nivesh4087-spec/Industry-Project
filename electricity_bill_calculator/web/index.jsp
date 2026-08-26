<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Electricity Bill Calculator - JSP & Servlet</title>
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

            .slab-badge {
                background: #0284c7;
                color: white;
                border-radius: 6px;
                padding: 4px 10px;
                font-weight: 600;
            }

            .form-control,
            .form-select {
                background-color: #0f172a;
                border-color: #334155;
                color: #f8fafc;
            }

            .form-control:focus,
            .form-select:focus {
                background-color: #1e293b;
                border-color: #38bdf8;
                color: #f8fafc;
                box-shadow: 0 0 0 0.25rem rgba(56, 189, 248, 0.25);
            }
        </style>
    </head>

    <body class="py-5">

        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-8">
                    <div class="card card-custom p-4">
                        <div
                            class="d-flex align-items-center justify-content-between mb-4 pb-3 border-bottom border-secondary">
                            <div>
                                <h2 class="fw-bold text-info mb-1"><i class="fa-solid fa-bolt me-2"></i>Electricity Bill
                                    Calculator</h2>
                                <p class="text-secondary mb-0">Powered by Java Servlet & JSP Engine</p>
                            </div>
                            <span class="badge bg-success px-3 py-2 fs-6">Live Tariff v2.4</span>
                        </div>

                        <% String errorMsg=(String) request.getAttribute("errorMessage"); if (errorMsg !=null) { %>
                            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                                <i class="fa-solid fa-triangle-exclamation me-2"></i>
                                <%= errorMsg %>
                                    <button type="button" class="btn-close btn-close-white"
                                        data-bs-dismiss="alert"></button>
                            </div>
                            <% } %>

                                <!-- Slab Info Banner -->
                                <div class="card bg-dark border-info mb-4">
                                    <div class="card-body">
                                        <h6 class="text-info fw-bold mb-3"><i
                                                class="fa-solid fa-layer-group me-2"></i>Tariff Rate Slab Structure</h6>
                                        <div class="row text-center g-2">
                                            <div class="col-6 col-md-3">
                                                <div class="p-2 border border-secondary rounded">
                                                    <div class="text-secondary small">First 50 Units</div>
                                                    <div class="fw-bold text-success">₹3.50 / unit</div>
                                                </div>
                                            </div>
                                            <div class="col-6 col-md-3">
                                                <div class="p-2 border border-secondary rounded">
                                                    <div class="text-secondary small">51 - 150 Units</div>
                                                    <div class="fw-bold text-warning">₹4.00 / unit</div>
                                                </div>
                                            </div>
                                            <div class="col-6 col-md-3">
                                                <div class="p-2 border border-secondary rounded">
                                                    <div class="text-secondary small">151 - 250 Units</div>
                                                    <div class="fw-bold text-danger">₹5.20 / unit</div>
                                                </div>
                                            </div>
                                            <div class="col-6 col-md-3">
                                                <div class="p-2 border border-secondary rounded">
                                                    <div class="text-secondary small">Above 250 Units</div>
                                                    <div class="fw-bold text-info">₹6.50 / unit</div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Input Form -->
                                <form action="CalculateBillServlet" method="post" id="billForm">
                                    <div class="row g-3">
                                        <div class="col-md-6">
                                            <label class="form-label text-light fw-medium"><i
                                                    class="fa-solid fa-user me-2 text-info"></i>Customer Name</label>
                                            <input type="text" name="customerName" class="form-control"
                                                placeholder="e.g. John Doe" required>
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label text-light fw-medium"><i
                                                    class="fa-solid fa-id-card me-2 text-info"></i>Consumer
                                                Number</label>
                                            <input type="text" name="consumerNo" class="form-control"
                                                placeholder="e.g. ELEC-98765" required>
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label text-light fw-medium"><i
                                                    class="fa-solid fa-plug me-2 text-info"></i>Connection
                                                Category</label>
                                            <select name="connectionType" class="form-select">
                                                <option value="Domestic" selected>Domestic (Standard Slab)</option>
                                                <option value="Commercial">Commercial (+25% Tariff)</option>
                                                <option value="Industrial">Industrial (+50% Tariff)</option>
                                            </select>
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label text-light fw-medium"><i
                                                    class="fa-solid fa-gauge-high me-2 text-info"></i>Electricity Units
                                                Consumed (kWh)</label>
                                            <input type="number" step="0.1" min="0" name="units" id="unitsInput"
                                                class="form-control" placeholder="e.g. 275.5" required>
                                        </div>
                                    </div>

                                    <div class="mt-4 text-end">
                                        <button type="submit" class="btn btn-info btn-lg px-5 text-dark fw-bold">
                                            <i class="fa-solid fa-calculator me-2"></i>Calculate Bill Total
                                        </button>
                                    </div>
                                </form>
                    </div>
                </div>
            </div>
        </div>

        <!-- jQuery & Bootstrap JS -->
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>

    </html>