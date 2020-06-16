# -*- encoding: utf-8 -*-
{
    "name": "Customer Credit Limit - Delivered Quantity(Override)",
    "version": "12.0.1.0.0",
    "summary": "",
    "license": "OPL-1",
    "depends": ["base","stock","oi_credit_limit_delivered_qty_with_peroid","account"],
    "author": "Oodu Implementers Private Limited",
    "website": "https://www.odooimplementers.com",
    "category": "Account & Stock",
    "description": "This module is to calculate the credit limit for the customer based on delivered quantity with override in delivery order.",
    "data": [
        "security/security.xml",
        "views/picking.xml",
    ],
    "images": ['static/description/banner.gif'],
    "active": False,
    "installable": True,
    
}
