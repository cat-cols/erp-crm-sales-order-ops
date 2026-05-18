-- Salesforce orders missing matching Business Central sales order
SELECT sf.order_id, sf.account_id, sf.order_date, sf.order_total
FROM sf_orders sf
LEFT JOIN bc_sales_orders bc
  ON sf.order_id = bc.external_crm_order_id
WHERE bc.external_crm_order_id IS NULL;