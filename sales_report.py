from odoo import api, fields, models
from datetime import date

class CustomModel(models.Model):
    _name = 'custom.model'

    @api.model
    def first_order_date(self):
        sale_order = self.env['sale.order'].search([], limit=1, order='date_order')
        return sale_order.date_order.date() if sale_order else None


class ProductSalesReport(models.Model):
    _name = 'product.sales.report'
    _description = 'Product Sales Report'


    name = fields.Char(required = True)
    age = fields.Integer(string = "Age")
    job_title = fields.Char(string = "Job Title")
    experience = fields.Char(string = "Experience")
    phone = fields.Char(string = "Phone")
    email = fields.Char(string = "Email")
    date_start = fields.Date(string = "Start Date",default = lambda self:self.env['custom.model'].first_order_date())
    date_end = fields.Date(string = "End Date",default = fields.Date.context_today)
    image_1920 = fields.Image("Image 1024", max_width=1920, max_height=1920, store=True)

    def get_best_selling_products(self,date_start,date_end):
        sales = self.env['sale.order'].search([
            ('date_order', '>=', date_start),
            ('date_order', '<=', date_end),
            ('order_line.product_id.sale_ok', '=', True),
            ('state','=','sale')
        ])

        product_names = {}
        for sale in sales:
            for sale_id in sale.order_line:
                if sale_id.product_id.id not in product_names:
                    product_names[sale_id.product_id.id] = {
                        'code':sale.name,
                        'name': sale_id.product_id.name,
                        'quantity': sale_id.product_uom_qty,
                        'revenue': sale_id.price_subtotal,
                        'date_order':sale.date_order,
                        'category':sale_id.product_id.categ_id.name,
                    }
                else:
                    product_names[sale_id.product_id.id]['quantity'] += sale_id.product_uom_qty
                    product_names[sale_id.product_id.id]['revenue'] += sale_id.price_subtotal

        products_sorted = sorted(product_names.values(), key=lambda x: x['quantity'], reverse=True)

        return products_sorted

    # def first_order_date(self):
    #     sale_order = self.env['sale.order'].search([])
    #     return [date.date_order.date() for date in sale_order][::-1][0]
















    def my_get_best_selling_products(self,date_start,date_end):
        sales = self.env['sale.order'].search([
            ('date_order','>=',date_start),
            ('date_order','<=',date_end),
            ('order_line.product_id.type', '=', 'product'),
            ('order_line.product_id.sale_ok','=',True)
        ])
        product_names = {}
        for sale in sales:
            for sale_id in sale.order_line:
                if sale_id.product_id.id not in product_names:
                    product_names[sale_id.product_id.id]={
                        'name':sale_id.product_id.name,
                        'quantity':sale_id.product_uom_qty,
                        'revenue':sale_id.price_subtotal,
                    }
                else:
                    product_names[sale_id.product_id.id]['quantity'] += sale_id.product_uom_qty
                    product_names[sale_id.product_id.id]['revenue'] += sale_id.price_subtotal

        products_sorted = sorted(product_names.values(), key=lambda x: x['quantity'], reverse=True)

        return products_sorted

    def get_best_selling_products_chat_gpt(self, date_start, date_end):
        # Get all the product sales within the specified date range
        sales = self.env['sale.order.line'].search([
            ('order_id.date_order', '>=', date_start),
            ('order_id.date_order', '<=', date_end),
            ('product_id.type', '=', 'product'),
            ('product_id.sale_ok', '=', True),
        ])
        # Calculate the total sales quantity and revenue for each product
        product_data = {}
        for sale in sales:
            if sale.product_id.id not in product_data:
                product_data[sale.product_id.id] = {
                    'name': sale.product_id.name,
                    'sales_qty': sale.product_uom_qty,
                    'revenue': sale.price_subtotal,
                }
            else:
                product_data[sale.product_id.id]['sales_qty'] += sale.product_uom_qty
                product_data[sale.product_id.id]['revenue'] += sale.price_subtotal

        # Sort the products by sales quantity in descending order
        products_sorted = sorted(product_data.values(), key=lambda x: x['sales_qty'], reverse=True)

        return products_sorted

    def get_best_purchasing_products(self, date_start, date_end):
        query = """
            SELECT 
                pt.name, 
                SUM(pol.product_qty) AS total_qty 
            FROM 
                purchase_order_line AS pol 
                JOIN purchase_order AS po ON pol.order_id = po.id 
                JOIN product_template AS pt ON pol.product_tmpl_id = pt.id 
            WHERE 
                po.date_order >= %s AND po.date_order <= %s 
                AND pt.active = True 
            GROUP BY 
                pt.name 
            ORDER BY 
                total_qty DESC
            """
        self.env.cr.execute(query, (date_start, date_end))
        result = self.env.cr.fetchall()
        return result


    def sql(self):
        start = '2023-04-01'
        end = '2023-05-12'
        print(self.get_best_purchasing_products(start,end))











class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def calculate_product_sales_report(self):
        product_sales_report = self.env['product.sales.report']

        for product in self.search([]):
            sales = self.env['sale.order.line'].search([
                ('product_id', '=', product.id),
                ('state', 'in', ['sale', 'done']),
            ])
            total_sales = sum(sales.mapped('price_total'))
            qty_sold = sum(sales.mapped('product_uom_qty'))

            product_sales_report.create({
                'product_id': product.id,
                'total_sales': total_sales,
                'qty_sold': qty_sold,
            })

        return True

