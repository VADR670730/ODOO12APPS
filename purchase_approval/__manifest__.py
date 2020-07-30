# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution	
#    Copyright (C) 2004-2008 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Purchase order Approval',
    'version': '12.0.1.0.0',
    'category': 'sales',
    'summary': 'In the purchase order form of the total amount value consider in purchase approval seetings of the minimum and maximum values based on approval to allocated to the perticular level users.',
    'author': 'Oodu Implementers Private Limited',
    'license': 'OPL-1',
    'website': 'https://www.odooimplementers.com',
    'description': 'This module allows In the purchase order form of the total amount its based on confirm the purchase order in purchase approval seeting of minimum and maximum value',
    'depends': ['purchase'],
    "data": [
        "views/purchase_view.xml",
        "views/purchase_approval_view.xml",
        "security/ir.model.access.csv",
        "security/purchase_group.xml",
        "data/ir_sequence_data.xml",

    ],
    'images': ['static/description/icon.png'],
    'auto_install': False,
    'installable': True,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
