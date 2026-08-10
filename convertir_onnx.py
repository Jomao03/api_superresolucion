import torch
import torch.nn as nn

# 1. Simulamos la estructura básica de un modelo de superresolución
class ModeloSimulado(nn.Module):
    def __init__(self):
        super(ModeloSimulado, self).__init__()
        self.conv = nn.Conv2d(3, 3, kernel_size=3, padding=1)
        
    def forward(self, x):
        return self.conv(x)

def exportar_modelo():
    print("Cargando el modelo original de PyTorch...")
    modelo = ModeloSimulado()
    modelo.eval() # Modo evaluación (obligatorio para exportar)

    # 2. Creamos un tensor "falso" con la forma de una imagen satelital de entrada
    # (Batch Size: 1, Canales: 3, Alto: 256, Ancho: 256)
    entrada_ejemplo = torch.randn(1, 3, 256, 256)

    print("Exportando a formato ONNX...")
    # 3. Realizamos la exportación
    torch.onnx.export(
        modelo,                     # El modelo cargado
        entrada_ejemplo,            # La imagen de ejemplo
        "modelo_optimizado.onnx",   # El nombre del archivo de salida
        export_params=True,         # Guardar los pesos entrenados
        opset_version=11,           # Versión de compatibilidad
        input_names=['entrada'],    # Nombre del nodo de entrada
        output_names=['salida'],    # Nombre del nodo de salida
        dynamic_axes={              # Permite que el tamaño de la imagen pueda variar luego
            'entrada': {0: 'batch_size', 2: 'height', 3: 'width'},
            'salida': {0: 'batch_size', 2: 'height', 3: 'width'}
        }
    )
    print("¡Exportación exitosa! Archivo guardado como 'modelo_optimizado.onnx'")

if __name__ == "__main__":
    exportar_modelo()