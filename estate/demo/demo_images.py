from odoo import api, SUPERUSER_ID

def create_demo_images(env):
    """Crear imágenes de prueba para el módulo estate"""
    
    # Imagen de prueba en base64 (una imagen simple de 1x1 pixel)
    demo_image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
    # Crear imágenes de prueba
    demo_images = [
        {
            'name': 'Fachada Principal',
            'description': 'Vista frontal de la propiedad',
            'image_type': 'exterior',
            'sequence': 1,
            'image': demo_image_base64
        },
        {
            'name': 'Sala de Estar',
            'description': 'Interior moderno y espacioso',
            'image_type': 'interior',
            'sequence': 2,
            'image': demo_image_base64
        },
        {
            'name': 'Plano de la Casa',
            'description': 'Distribución completa',
            'image_type': 'floorplan',
            'sequence': 3,
            'image': demo_image_base64
        }
    ]
    
    # Crear las imágenes
    for demo_data in demo_images:
        env['estate.image'].create(demo_data)
    
    print("✅ Imágenes de prueba creadas exitosamente")

if __name__ == "__main__":
    env = api.Environment(api.Environment.manage(), SUPERUSER_ID, {})
    create_demo_images(env) 