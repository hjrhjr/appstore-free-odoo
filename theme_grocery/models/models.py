# -*- coding: utf-8 -*-

import json
from odoo import models, fields, api, SUPERUSER_ID


class website(models.Model):
    _inherit = 'website'

    def get_categories(self):
        categories = self.env['product.public.category'].sudo().search([])
        return categories

    def get_homepage_categories(self):
        categories = self.env['homepage.categories'].sudo().search([], order='sequence')
        return categories.mapped('category_id')

    def get_homepage_sliders(self):
        sliders = self.env['homepage.slider'].sudo().search([], order='sequence')
        return sliders

    def get_homepage_horizontal_banner(self):
        banners = self.env['homepage.horizontal.banner'].sudo().search([], order='sequence')
        return banners

    def get_homepage_vertical_banner(self):
        banners = self.env['homepage.vertical.banner'].sudo().search([], limit=1)
        return banners

    def get_homepage_horizontal_full_banner(self):
        banners = self.env['homepage.horizontal.full.banner'].sudo().search([], limit=1)
        return banners

    def get_homepage_horizontal_half_banner(self):
        banners = self.env['homepage.horizontal.half.banner'].sudo().search([], limit=2)
        return banners

    def get_testimonials(self):
        testimonials = self.env['customer.testimonial'].sudo().search([], order='sequence')
        return testimonials

    def get_bestseller_products(self):
        products = self.env['bestseller.product'].sudo().search([], order='sequence')
        return products.mapped('product_tmpl_id')

    def get_featured_products(self):
        products = self.env['featured.product'].sudo().search([], order='sequence')
        return products.mapped('product_tmpl_id')

    def get_latest_products(self):
        products = self.env['latest.product'].sudo().search([], order='sequence')
        return products.mapped('product_tmpl_id')

    def get_latest_blog_posts(self):
        blog_posts = self.env['blog.post'].sudo().search(
            [('website_published', '=', True)], order='id DESC')
        return blog_posts

    def get_cover_image(self, blog_post):
        return json.loads(blog_post.cover_properties).get('background-image')[4:-1]

    def get_product_avg_rating(self, product):
        if product.sudo().rating_ids:
            total_rating = product.sudo().rating_ids.mapped('rating')
            return sum(total_rating) / len(product.sudo().rating_ids)
        else:
            return 0


class HomepageCategories(models.Model):
    _name = 'homepage.categories'
    _description = "shows homepage categories details."
    _rec_name = 'category_id'
    _order = 'sequence'

    category_id = fields.Many2one('product.public.category', string='Category')
    sequence = fields.Integer('Sequence', default=10)


class HomepageSlider(models.Model):
    _name = 'homepage.slider'
    _description = "shows homepage slider details."
    _order = 'sequence'

    name = fields.Char('Name')
    image = fields.Binary('Slider Image', help="Slider image size must be 938px x 437px.")
    link = fields.Char('Link')
    sequence = fields.Integer('Sequence', default=10)
    rtl_image = fields.Binary('Slider Image (RTL)', help="Slider image size must be 938px x 437px.")


class HomepageHorizontalBanner(models.Model):
    _name = 'homepage.horizontal.banner'
    _description = "shows homepage horizontal banner details."
    _order = 'sequence'

    name = fields.Char('Name (Label)')
    sub_heading = fields.Char('Sub Heading')
    image = fields.Binary('Background Image', help='Image size must be 358px x 275px.')
    link = fields.Char('Link')
    sequence = fields.Integer('Sequence', default=10)
    rtl_image = fields.Binary('Slider Image (RTL)', help="Slider image size must be 358px x 275px.")


class BestsellerProduct(models.Model):
    _name = 'bestseller.product'
    _description = "shows bestseller product in store."
    _order = 'sequence'

    product_tmpl_id = fields.Many2one('product.template', string='Product')
    sequence = fields.Integer('Sequence', default=10)


class FeaturedProduct(models.Model):
    _name = 'featured.product'
    _description = "shos featured product in store."
    _order = 'sequence'

    product_tmpl_id = fields.Many2one('product.template', string='Product')
    sequence = fields.Integer('Sequence', default=10)


class LatestProduct(models.Model):
    _name = 'latest.product'
    _description = "shows latest product in store."
    _order = 'sequence'

    product_tmpl_id = fields.Many2one('product.template', string='Product')
    sequence = fields.Integer('Sequence', default=10)


class HomepageHorizontalFullBanner(models.Model):
    _name = 'homepage.horizontal.full.banner'
    _description = "shows homepage horizontal full banner details."

    name = fields.Char('Name')
    link = fields.Char('Link')
    image = fields.Binary('Banner Image', help='Bammer must be 938px x 173px size.')
    rtl_image = fields.Binary('Banner Image (RTL)', help='Bammer must be 938px x 173px size.')


class HomepageHorizontalHalfBanner(models.Model):
    _name = 'homepage.horizontal.half.banner'
    _description = "shows homepage horizontal half banner details."

    name = fields.Char('Name')
    link = fields.Char('Link')
    image = fields.Binary('Banner Image', help='Bammer must be 454px x 165px size.')
    rtl_image = fields.Binary('Banner Image (RTL)', help='Bammer must be 454px x 165px size.')


class HomepageVerticalBanner(models.Model):
    _name = 'homepage.vertical.banner'
    _description = "shows homepage vertical banner details."

    name = fields.Char('Name')
    link = fields.Char('Link')
    image = fields.Binary('Banner Image', help='Bammer must be 285px x 458px size.')
    rtl_image = fields.Binary('Banner Image (RTL)', help='Bammer must be 285px x 458px size.')


class CustomerTestimonial(models.Model):
    _name = 'customer.testimonial'
    _description = "show customers testimony about services."
    _order = 'sequence'

    name = fields.Char('Customer Name', required=True)
    image = fields.Binary('Customer Photo')
    review = fields.Text('Review', required=True)
    sequence = fields.Integer('Sequence', default=10)


class IrModuleModule(models.Model):
    _name = "ir.module.module"
    _description = 'Module'
    _inherit = _name

    @api.model
    def _theme_remove(self, website):
        if website.theme_id.name == "theme_grocery":
            # default homepage set when un-install theme grocery
            env = api.Environment(self.env.cr, SUPERUSER_ID, {})
            default_website = env.ref('website.default_website', raise_if_not_found=False)
            default_homepage = env.ref('website.homepage_page', raise_if_not_found=False)
            default_website.homepage_id = default_homepage.id
        return super(IrModuleModule, self)._theme_remove(website)
