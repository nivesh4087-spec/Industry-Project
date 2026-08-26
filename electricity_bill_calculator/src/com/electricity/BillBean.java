package com.electricity;

import java.io.Serializable;

public class BillBean implements Serializable {
    private String customerName;
    private String consumerNo;
    private String connectionType;
    private double totalUnits;
    
    // Slab breakdown units
    private double slab1Units; // 0 - 50
    private double slab2Units; // 51 - 150
    private double slab3Units; // 151 - 250
    private double slab4Units; // > 250
    
    // Slab breakdown costs
    private double slab1Cost;
    private double slab2Cost;
    private double slab3Cost;
    private double slab4Cost;
    
    // Charges and Totals
    private double energyCharges;
    private double fixedCharge;
    private double electricityDuty;
    private double totalBillAmount;
    private double earlyPaymentDiscount;
    private double latePaymentAmount;

    public BillBean() {}

    // Getters and Setters
    public String getCustomerName() { return customerName; }
    public void setCustomerName(String customerName) { this.customerName = customerName; }

    public String getConsumerNo() { return consumerNo; }
    public void setConsumerNo(String consumerNo) { this.consumerNo = consumerNo; }

    public String getConnectionType() { return connectionType; }
    public void setConnectionType(String connectionType) { this.connectionType = connectionType; }

    public double getTotalUnits() { return totalUnits; }
    public void setTotalUnits(double totalUnits) { this.totalUnits = totalUnits; }

    public double getSlab1Units() { return slab1Units; }
    public void setSlab1Units(double slab1Units) { this.slab1Units = slab1Units; }

    public double getSlab2Units() { return slab2Units; }
    public void setSlab2Units(double slab2Units) { this.slab2Units = slab2Units; }

    public double getSlab3Units() { return slab3Units; }
    public void setSlab3Units(double slab3Units) { this.slab3Units = slab3Units; }

    public double getSlab4Units() { return slab4Units; }
    public void setSlab4Units(double slab4Units) { this.slab4Units = slab4Units; }

    public double getSlab1Cost() { return slab1Cost; }
    public void setSlab1Cost(double slab1Cost) { this.slab1Cost = slab1Cost; }

    public double getSlab2Cost() { return slab2Cost; }
    public void setSlab2Cost(double slab2Cost) { this.slab2Cost = slab2Cost; }

    public double getSlab3Cost() { return slab3Cost; }
    public void setSlab3Cost(double slab3Cost) { this.slab3Cost = slab3Cost; }

    public double getSlab4Cost() { return slab4Cost; }
    public void setSlab4Cost(double slab4Cost) { this.slab4Cost = slab4Cost; }

    public double getEnergyCharges() { return energyCharges; }
    public void setEnergyCharges(double energyCharges) { this.energyCharges = energyCharges; }

    public double getFixedCharge() { return fixedCharge; }
    public void setFixedCharge(double fixedCharge) { this.fixedCharge = fixedCharge; }

    public double getElectricityDuty() { return electricityDuty; }
    public void setElectricityDuty(double electricityDuty) { this.electricityDuty = electricityDuty; }

    public double getTotalBillAmount() { return totalBillAmount; }
    public void setTotalBillAmount(double totalBillAmount) { this.totalBillAmount = totalBillAmount; }

    public double getEarlyPaymentDiscount() { return earlyPaymentDiscount; }
    public void setEarlyPaymentDiscount(double earlyPaymentDiscount) { this.earlyPaymentDiscount = earlyPaymentDiscount; }

    public double getLatePaymentAmount() { return latePaymentAmount; }
    public void setLatePaymentAmount(double latePaymentAmount) { this.latePaymentAmount = latePaymentAmount; }
}