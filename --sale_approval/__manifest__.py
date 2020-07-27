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
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

{
    'name': 'Sales order Approval',
    'version': '13.0.1.0.0',
    'category': 'sales',
    'summary': 'In the sale order form of the total amount value consider in sale approval seetings of the minimum and maximum values based on approval to allocated to the perticular level users.',
    'author': 'Oodu Implementers Private Limited',
    'license': 'OPL-1',
    'website': 'https://www.odooimplementers.com',
    'description': 'This module allows In the sale order form of the total amount its based on confirm the sale order in sale approval seeting of minimum and maximum value',
    'depends': ['sale'],
    'data': [
        'views/sale_view.xml',
        'views/sale_approval_view.xml',
        "security/ir.model.access.csv",
        "security/sale_group.xml",
        "data/ir_sequence_data.xml",
    ],
    'images': ['static/description/icon.png'],
    'auto_install': False,
    'installable': True,
    'application': False,
}
