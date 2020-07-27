# -*- encoding: utf-8 -*-
{
    "name": "Customer Credit & Days & Invoice Limit - Ordered Quantity",
    "version": "12.0.1.0.0",
    "summary": "",
    "license": "OPL-1",
    "depends": ["base", "sale", "stock","account"],
    "author": "Oodu Implementers Private Limited",
    "website": "https://www.odooimplementers.com",
    "category": "Account & Sale & Stock",
    "description": "This module is to calculate the credit limit and days limit and invoice limit for the customer based on ordered quantity",
    "data": [
        "wizard/credit_limit_warning.xml",
        "views/partner.xml",
        "security/security.xml",
        "security/ir.model.access.csv"
    ],
    "images": ['static/description/banner.gif'],
    "active": False,
    "installable": True,
}