from odoo import fields, models,_
from odoo.exceptions import UserError
from datetime import datetime
class QuickModelUpgrade(models.TransientModel):
    _name='quick.model.upgrade' 
    
    def get_recent_modules(self):
        return self.env['modules.upgrade.history'].search([('last_update_module_date','!=',False)],order="last_update_module_date desc",limit=5).ids
    
    module_ids = fields.Many2many('ir.module.module','quick_modele_upgrade_ir_mudule_rel','wizard_id','module_id',string='Modules')  
    recent_module_ids = fields.Many2many('modules.upgrade.history','quick_modele_upgrade_modules_upgrade_history_rel','wizard_id','module_id',string='Recent Upgraded Modules',default=get_recent_modules)
    
    def upgrade_button(self):
        if not self.module_ids:
            raise UserError(_('No Modules Selected for upgrade!!'))
        else:    
            for module_obj in self.module_ids:
                module_obj.button_immediate_upgrade()
                history_record=self.env['modules.upgrade.history'].search([('module_id','=',module_obj.id)])
                if history_record:
                    for record in history_record:
                        record.write({'last_update_module_date':datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')})
                else:
                    self.env['modules.upgrade.history'].create({'last_update_module_date':datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S'),'module_id':module_obj.id})    
        return  
    
   
    def button_immediate_upgrade(self):
        self.module_ids.button_immediate_upgrade();
        