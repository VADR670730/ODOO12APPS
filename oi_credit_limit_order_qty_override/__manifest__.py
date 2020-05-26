# -*- encoding: utf-8 -*-
{
"name": "Customer Credit Limit - Ordered Quantity(Override)",
    "version": "12.0.1.0.0",
    "summary": "",
    "license": "OPL-1",
    "depends": ["base","oi_credit_limit_order_qty_with_invoice","account"],
    "author": "Oodu Implementers Private Limited",
    "website": "https://www.odooimplementers.com",
    "category": "Account",
    "description": "This module is to calculate the credit limit for the customer based on ordered quantity with override in Invoice",
    "data": [
        "security/security.xml",
        "views/invoice.xml"
    ],
    "images": ['static/description/banner.gif'],
    "active": False,
    "installable": True,
}
