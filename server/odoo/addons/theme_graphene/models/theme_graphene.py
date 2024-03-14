from odoo import models


class ThemeGraphene(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_graphene_post_copy(self, mod):
        self.enable_view('website.template_header_contact')
        self.enable_header_off_canvas()

        self.enable_view('website.template_footer_centered')

        self.enable_asset('Ripple effect SCSS')
        self.enable_asset('Ripple effect JS')
