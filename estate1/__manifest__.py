{
    'name': 'Real Estate 1',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'], 
    'data':[
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/property_offer_view.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_menu.xml',
        'views/inherited_model_view.xml',
        'data/data_property_type.xml',
        'data/data_property_tags.xml'
    ],
    'application': True
}