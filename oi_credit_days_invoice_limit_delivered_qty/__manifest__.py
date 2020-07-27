# -*- encoding: utf-8 -*-
{
    "name": "Customer Credit & Days & Invoice Limit - Delivered Quantity",
    "version": "12.0.1.0.0",
    "summary": "",
    "license": "OPL-1",
    "depends": ["base", "sale", "stock",],
    "author": "Oodu Implementers Private Limited",
    "website": "https://www.odooimplementers.com",
    "category": "Sale & Stock",
    "description": "This module is to calculate the credit limit and days limit and invoice limit for the customer based on delivered Quantity",
    "data": [
        "wizard/credit_limit_warning.xml",
        "views/partner.xml",
		"security/ir.model.access.csv",
        "security/security.xml",
    ],
    "images": ['static/description/banner.gif'],
    "active": False,
    "installable": True,
}
