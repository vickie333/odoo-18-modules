{
    'name': 'Real Estate Images',
    'version': '18.0.1.0.0',
    'category': 'Real Estate',
    'summary': 'Images of each inmobiliary',
    'description': """
        This module provides a kanban view for pictures of each estate.
    """,    
    'author': 'Vickie',
    'data': [
        'views/estate_property_image_views.xml',
        'security/ir.model.access.csv',
    ],
    'depends': ['estate'],
}
