
{
    'name': 'Real Estate',
    'version': '18.0.1.0.0',
    'category': 'Real Estate',
    'summary': 'Real Estate',
    'description': 'Real Estate',
    'author': 'Vickie',
    'depends': ['base','mail'],
    "data": [
        "data/data_estate_category.xml",
        "security/ir.model.access.csv",
        "views/estate_image_views.xml",
        "views/estate_views.xml",
        "reports/report_template.xml",
        "reports/report.xml",
        "report/paperformat.xml"
    ],
    'demo': [
        'demo/demo.xml'
    ],
    'application': True
}