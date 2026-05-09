# Sales Data Coordinator — Order Lifecycle & Data Quality System
- Microsoft Business Central ERP + Salesforce CRM Order Operations

## Project Purpose

This project simulates a Sales Data Coordinator workflow using Microsoft Dynamics 365 Business Central as the ERP/order management system and Salesforce as the CRM/account management system. The project demonstrates sales order entry, order edits, fulfillment coordination, invoicing, credit memo processing, returns/refusals, CRM-to-ERP data integrity, discrepancy resolution, dashboard/report support, and SOP documentation.

This project simulates the operational workflows of a Sales Data Coordinator supporting a fast-growing CPG/cannabis business. The goal is to demonstrate readiness for work involving sales order entry, order edits, fulfillment coordination, invoicing, credit memo processing, account data quality, CRM/ERP reconciliation, exception tracking, and basic operational reporting.

The project is designed around the responsibilities of a Sales Data Coordinator role: maintaining clean sales order data, coordinating across Sales, Distribution, Inventory, and Accounting, and supporting accurate, timely, compliant order execution.

I created a Salesforce Trailhead Playground to simulate CRM account management, imported account/customer data, configured fields relevant to order eligibility, then reconciled the CRM export against ERP-style sales order data in PostgreSQL.

## Business Scenario

A multi-state cannabis edibles company receives sales orders from customers across multiple markets. Orders are entered into an ERP-style order management process, supported by CRM account data, inventory availability, shipment tracking, invoicing, and exception handling.

Common operational issues include:

- Missing or invalid customer account data
- CRM accounts that do not match ERP customer records
- Orders placed for inactive or non-compliant accounts
- SKU or state availability mismatches
- Inventory shortages and backorders
- Rejected, returned, or refused orders
- Invoice totals that do not match fulfilled order totals
- Credit memos created for short shipments, refusals, returns, or pricing errors
- Open exceptions requiring follow-up from Sales, Distribution, Inventory, or Accounting

## Project Modules

### 1. Sales Order Lifecycle Management

Simulates the full order lifecycle:

1. Order entered
2. Order edited or approved
3. Inventory checked
4. Order fulfilled or backordered
5. Shipment created
6. Invoice issued
7. Credit memo or return processed if needed
8. Order closed

### 2. CRM-to-ERP Account Reconciliation

Compares CRM-style account records to ERP-style customer records to identify master data issues that could block clean order execution.

Example checks:

- CRM account missing ERP customer ID
- ERP customer missing CRM owner
- Account name mismatch
- Missing billing terms
- Customer on credit hold
- Inactive account with open orders
- Missing license or compliance status

### 3. Order Exception Reporting

Creates a structured exception tracker for rejected orders, returns, refusals, backorders, invoice mismatches, and credit memo issues.

The reporting layer is designed to answer:

- Which orders need follow-up?
- Which team owns the issue?
- Which issues are blocking fulfillment or invoicing?
- How many credit memos were created by reason?
- Which states, customers, or SKUs create the most exceptions?

## Source Systems Simulated

| Source | Business Function | Example Data |
|---|---|---|
| CRM Accounts | Sales / Account ownership | Account status, sales rep, market, contact fields |
| ERP Customers | Order management / billing | Customer ID, billing terms, credit hold, license status |
| Sales Orders | Order entry | Order headers, order dates, status, customer IDs |
| Sales Order Lines | Order details | SKU, quantity, unit price, discounts |
| Inventory Snapshot | Inventory availability | SKU, state, warehouse, available units |
| Shipments | Distribution | Fulfilled quantity, shipped date, delivery/refusal status |
| Invoices | Accounting | Invoice amount, invoice date, payment status |
| Credit Memos | Accounting / Exceptions | Credit reason, amount, linked invoice/order |

## Key Skills Demonstrated

| Job responsibility                                      | Project evidence                                                            |
| ------------------------------------------------------- | --------------------------------------------------------------------------- |
| Order lifecycle management                              | Business Central sales order workflow from entry to invoice/credit memo     |
| Entry, edits, fulfillment, invoicing, credit memos      | Screenshots + SOPs + order tracker workbook                                 |
| Additions, rejections, returns, refusals                | Order modification SOP and exception reason code log                        |
| State-specific compliance                               | Compliance matrix by state, customer license status, SKU eligibility checks |
| Accurate, timely, compliant order activity              | Daily follow-up queue and order status dashboard                            |
| Maintain data across ERP/CRM/external systems           | Salesforce + Business Central exports reconciled in workbook                |
| Identify and resolve discrepancies                      | CRM-to-ERP reconciliation tab and exception tracker                         |
| Partner with Sales, Distribution, Inventory, Accounting | Owner team fields, escalation notes, response templates                     |
| Customer support                                        | Customer support response templates and order status documentation          |
| Power user of ERP/CRM tools                             | Business Central and Salesforce screenshots/notes                           |
| Reporting and dashboard maintenance                     | Order status, exception, and data quality dashboards                        |
| SOP documentation                                       | Order lifecycle SOP, credit memo SOP, data quality checklist                |
| Ad hoc reporting                                        | Daily follow-up queue and issue summary report                              |

- Sales order lifecycle understanding
- CRM/ERP-style data modeling
- Data entry validation
- Data quality checks
- Cross-functional exception tracking
- Account and customer master data reconciliation
- Basic operational reporting
- SQL-based QA/QC
- SOP and process documentation
- Dashboard-ready mart design

## Intended Audience

This project is designed for hiring managers evaluating readiness for Sales Data Coordinator, Sales Operations Coordinator, Data Coordinator, Business Operations Analyst, or entry-level Business Analyst roles.

## Portfolio Positioning

This project demonstrates the operational foundation behind analytics work. It shows the ability to work close to the business process before building higher-level reporting and analysis.

The project connects naturally to broader analytics work in the rest of this portfolio, including operations dashboards, data quality systems, reconciliation workflows, and forecasting.